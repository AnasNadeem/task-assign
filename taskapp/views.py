from django.shortcuts import get_object_or_404
from taskapp.models import Chat, Profile
from django.contrib.auth.models import User

def get_last_messages(chat_id):
    chat = get_object_or_404(Chat, code=chat_id)
    return chat.messages.order_by('-timestamp').all()[:20]

def get_user_profile(username):
    user = get_object_or_404(User, username=username)
    return get_object_or_404(Profile, user=user)

def get_chat_messages(chat_id):
    return get_object_or_404(Chat, code=chat_id)