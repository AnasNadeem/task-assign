from tastypie.resources import ModelResource
from taskapp.models import Task

class TaskResource(ModelResource):
    class Meta:
        queryset = Task.objects.all()
        resource_name = 'task'

        
