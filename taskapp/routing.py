from taskapp.consumers import ChatConsumer
from django.urls import path

websocket_urlpatterns = [
    path('ws/chat/<int:pk>', ChatConsumer.as_asgi()),
]
