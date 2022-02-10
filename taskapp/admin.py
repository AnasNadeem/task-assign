from django.contrib import admin
from taskapp.models import Task, Profile, FriendRequest, Message, Chat

# Register your models here.
admin.site.register(Task)
admin.site.register(Profile)
admin.site.register(FriendRequest)
admin.site.register(Message)
admin.site.register(Chat)
