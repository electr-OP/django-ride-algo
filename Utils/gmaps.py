import googlemaps
from django.conf import settings

# Initialize Google Maps client
gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

def get_eta(driver_location, pickup_location):
        """Fetch estimated time of arrival from Google Maps API"""
        response = gmaps.distance_matrix(
            origins=f"{driver_location.y},{driver_location.x}",
            destinations=f"{pickup_location.y},{pickup_location.x}",
            mode="driving"
        )
        try:
            return response["rows"][0]["elements"][0]["duration"]["value"] / 60  # Convert seconds to minutes
        except KeyError:
            return float("inf")  # No ETA available

def calculate_driver_score(driver, eta, passenger_prefs):
    """Calculate weighted score for each driver"""
    score = 0
    score += max(0, 10 - driver.distance.km) * 2  # Closer drivers get higher score
    score += driver.rating * 3  # Higher ratings are prioritized
    score += max(0, 10 - eta) * 5  # Shorter ETA is better

    # Match passenger preferences
    for key, value in passenger_prefs.items():
        if driver.preferences.get(key) == value:
            score += 2

    return score

def get_optimal_route(pickup_lat, pickup_lon, dropoff_lat, dropoff_lon):
        """
        Fetches the best navigation route from Google Maps API.
        """
        try:
            response = gmaps.directions(
                origin=f"{pickup_lat},{pickup_lon}",
                destination=f"{dropoff_lat},{dropoff_lon}",
                mode="driving",
                alternatives=True  # Get multiple route options
            )
            if not response:
                return None

            # Extract the best route based on duration
            best_route = min(response, key=lambda x: x["legs"][0]["duration"]["value"])

            return {
                "distance": best_route["legs"][0]["distance"]["text"],
                "duration": best_route["legs"][0]["duration"]["text"],
                "polyline": best_route["overview_polyline"]["points"],  # For map visualization
                "steps": [
                    {
                        "instruction": step["html_instructions"],
                        "distance": step["distance"]["text"],
                        "duration": step["duration"]["text"]
                    }
                    for step in best_route["legs"][0]["steps"]
                ]
            }
        except Exception as e:
            print(e, "Error")
            return None