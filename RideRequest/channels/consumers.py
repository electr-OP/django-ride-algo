import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache  # Use Redis cache for storing driver locations


class RideTrackingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        When a WebSocket connection is established.
        """
        self.ride_id = self.scope["url_route"]["kwargs"]["ride_id"]
        self.room_group_name = f"ride_{self.ride_id}"

        # Join ride group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """
        When a WebSocket connection is closed.
        """
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """
        Handle incoming location updates from driver.
        """
        data = json.loads(text_data)
        latitude = data["latitude"]
        longitude = data["longitude"]

        # Store driver location in Redis cache (TTL: 10 minutes)
        cache.set(
            f"driver_location_{self.ride_id}",
            {"lat": latitude, "lon": longitude},
            timeout=600,
        )

        # Broadcast location update to all clients
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "send_location_update",
                "latitude": latitude,
                "longitude": longitude,
            },
        )

    async def send_location_update(self, event):
        """
        Send real-time location update to all connected clients.
        """
        await self.send(
            text_data=json.dumps(
                {
                    "latitude": event["latitude"],
                    "longitude": event["longitude"],
                }
            )
        )
