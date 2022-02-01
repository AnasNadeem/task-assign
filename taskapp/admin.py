from django.contrib import admin
from taskapp.models import Task, Profile, FriendRequest

# Register your models here.
admin.site.register(Task)
admin.site.register(Profile)
admin.site.register(FriendRequest)