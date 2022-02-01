from django.urls import path, include
from taskapp.api import TaskResource, UserResource, FriendResource
from taskapp.authen_api import AuthResource

task_resource = TaskResource()
auth_resource = AuthResource()
user_resource = UserResource()
friend_resource = FriendResource()

urlpatterns = [
    path('', include(task_resource.urls)),
    path('', include(auth_resource.urls)),
    path('', include(user_resource.urls)),
    path('', include(friend_resource.urls)),
]
