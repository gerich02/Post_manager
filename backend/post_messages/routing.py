from django.urls import path
from .consumers import Messages

ws_urlpatterns = [
    path("ws/messages/", Messages.as_asgi()),
]
