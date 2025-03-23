import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from RideRequest.channels import routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ridesharing.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(routing.websocket_urlpatterns),
})
