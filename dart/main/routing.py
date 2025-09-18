from django.urls import path
from .consumers import MultiplayerConsumer, GameConsumer

websocket_urlpatterns = [
    path('ws/multiplayer/<uuid:game_id>/', MultiplayerConsumer.as_asgi()),
    path('ws/<uuid:game_id>/', GameConsumer.as_asgi()),
]