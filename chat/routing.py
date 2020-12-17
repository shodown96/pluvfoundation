# chat/routing.py
from django.urls import re_path
from django.conf import settings

from .consumers import ChatConsumer

# websocket_urlpatterns = [
#     re_path(r'^ws/chat/(?P<room_name>[^/]+)/$', ChatConsumer),
# ]
websocket_urlpatterns = [
    re_path(r'wss/chat/(?P<room_name>\w+)/$', ChatConsumer),
]
if settings.DEBUG:
    websocket_urlpatterns = [
        re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer),
    ]
# from django.urls import path
# from channels.routing import ProtocolTypeRouter, URLRouter
# from .consumers import LiveScoreConsumer
# websockets = URLRouter([
#     path(
#         "ws/live-score/<int:game_id>", LiveScoreConsumer,
#         name="live-score",
#     ),
# ])