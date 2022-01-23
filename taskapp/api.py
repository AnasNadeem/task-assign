from django.apps import AppConfig
from tastypie.resources import ModelResource
from taskapp.models import Task
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization

class TaskResource(ModelResource):
    class Meta:
        queryset = Task.objects.all()
        resource_name = 'task'
        authentication = ApiKeyAuthentication()
        authorization = Authorization()

    def obj_create(self, bundle, **kwargs):
        return super(TaskResource, self).obj_create(bundle, creator=bundle.request.user)

    def authorized_read_list(self, object_list, bundle):
        # IMPLEMNT - Also the user assigned can read and write 
        return object_list.filter(creator=bundle.request.user)