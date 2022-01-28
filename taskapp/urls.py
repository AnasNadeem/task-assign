from distutils.log import Log
from django.urls import path, include
from taskapp.api import TaskResource, UserResource
from taskapp.authen_api import AuthResource

task_resource = TaskResource()
auth_resource = AuthResource()
user_resource = UserResource()

urlpatterns = [
    path('', include(task_resource.urls)),
    path('', include(auth_resource.urls)),
    path('', include(user_resource.urls)),
]
