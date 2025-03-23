from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from RideRequest.models import RideRequest
from RideMatching.models import Driver
from RideRequest.serializers import RideRequestSerializer, NavigationRequestSerializer
from Utils.gmaps import get_eta, calculate_driver_score, get_optimal_route

class RideMatchingView(APIView):
    """
    API view to match ride requests with drivers
    """

    def post(self, request):
        serializer = RideRequestSerializer(data=request.data)
        if serializer.is_valid():
            pickup_lat = serializer.validated_data["pickup_lat"]
            pickup_lon = serializer.validated_data["pickup_lon"]
            passenger_prefs = serializer.validated_data["preferences"]

            pickup_location = Point(pickup_lon, pickup_lat, srid=4326)

            print(pickup_location)

            # Fetch nearby available drivers
            nearby_drivers = Driver.objects.filter(
                status="available"
            ).annotate(
                distance=Distance("location", pickup_location)
            ).order_by("distance")[:10]  # Get top 10 closest drivers

            best_driver = None
            best_score = -1

            for driver in nearby_drivers:
                eta = get_eta(driver.location, pickup_location)
                score = calculate_driver_score(driver, eta, passenger_prefs)

                if score > best_score:
                    best_score = score
                    best_driver = driver

            if best_driver:
                return Response({"message": "Driver found", "driver": {"id": best_driver.id, "name": best_driver.name}}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "No suitable driver found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class RideNavigationView(APIView):
    """
    API to determine the optimal route for ride.
    """
    def post(self, request):
        serializer = NavigationRequestSerializer(data=request.data)
        if serializer.is_valid():
            pickup_lat = serializer.validated_data["pickup_lat"]
            pickup_lon = serializer.validated_data["pickup_lon"]
            dropoff_lat = serializer.validated_data["dropoff_lat"]
            dropoff_lon = serializer.validated_data["dropoff_lon"]

            # Call Google Maps API for optimal route
            route = get_optimal_route(pickup_lat, pickup_lon, dropoff_lat, dropoff_lon)

            if route:
                return Response({"route": route}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "No route found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    