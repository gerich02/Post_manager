import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import post_messages.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "post_manager.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(post_messages.routing.ws_urlpatterns)
        ),
    }
)
