from distutils.log import Log
from django.urls import path, include
from taskapp.api import TaskResource
from taskapp.authen_api import AuthResource

task_resource = TaskResource()
auth_resource = AuthResource()

urlpatterns = [
    path('', include(task_resource.urls)),
    path('', include(auth_resource.urls)),
]
