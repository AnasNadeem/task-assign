from django.urls import path, include
from taskapp.api import TaskResource

task_resource = TaskResource()

urlpatterns = [
    path('', include(task_resource.urls)),
]
