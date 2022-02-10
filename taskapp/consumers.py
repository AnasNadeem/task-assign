from channels.generic.websocket import WebsocketConsumer
from .models import Chat, Message

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # Get the user and check if he is authnticated and is allowed in the room
        self.user = self.scope['user']  
        self.header = self.scope['headers']
        self.room_name = self.scope['url_route']['kwargs']['pk']
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        pass

    def disconnect(self, code):
        pass

    