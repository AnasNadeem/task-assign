from taskapp.consumers import ChatConsumer
from django.urls import path

websocket_urlpatterns = [
    path('ws/chat/<str:code>', ChatConsumer.as_asgi()),
]
