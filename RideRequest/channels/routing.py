from django.urls import path
from .consumers import RideTrackingConsumer

websocket_urlpatterns = [
    path("ws/ride/<str:ride_id>/", RideTrackingConsumer.as_asgi()),
]
