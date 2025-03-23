from rest_framework import serializers
from ..models.ride import RideRequest

class RideRequestSerializer(serializers.ModelSerializer):
    pickup_lat = serializers.FloatField(write_only=True)
    pickup_lon = serializers.FloatField(write_only=True)

    class Meta:
        model = RideRequest
        fields = ["passenger_id", "pickup_lat", "pickup_lon", "preferences"]


class NavigationRequestSerializer(serializers.Serializer):
    pickup_lat = serializers.FloatField()
    pickup_lon = serializers.FloatField()
    dropoff_lat = serializers.FloatField()
    dropoff_lon = serializers.FloatField()