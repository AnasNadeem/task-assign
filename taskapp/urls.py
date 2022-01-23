from distutils.log import Log
from django.urls import path, include
from taskapp.api import TaskResource
from taskapp.authen_api import RegisterResource, LoginResource

task_resource = TaskResource()
register_resource = RegisterResource()
login_resource = LoginResource()

urlpatterns = [
    path('', include(task_resource.urls)),
    path('', include(register_resource.urls)),
    path('', include(login_resource.urls)),
]
