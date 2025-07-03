from .consumers import ChatConsumer, PrivateChatConsumer
from django.urls import re_path


websocket_urlpatterns = [
    re_path(r"ws/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
    re_path(r"ws/private/(?P<chat_id>\w+)/$", PrivateChatConsumer.as_asgi())
]