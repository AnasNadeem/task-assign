import json
from channels.generic.websocket import WebsocketConsumer
from .models import Chat, Message
from asgiref.sync import async_to_sync
from taskapp.views import get_chat_messages, get_last_messages, get_user_profile

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['code']
        async_to_sync(self.channel_layer.group_add)(
            self.room_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        user_profile = get_user_profile(data['from'])
        message = Message.objects.create(
            sender_profile=user_profile,
            content=data['message']
        )
        chat = get_chat_messages(self.room_name)
        chat.messages.add(message)
        chat.save()
        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                'type':'chat.message',
                'message':self.message_to_json(message)
            }
        )

    def message_to_json(self, message):
        return {
            'id': message.id,
            'author': message.sender_profile.user.username,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }
    
    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))