from django.shortcuts import get_object_or_404
from taskapp.models import Chat

def get_last_messages(chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    return chat.messages.order_by('-timestamp').all()[:20]

