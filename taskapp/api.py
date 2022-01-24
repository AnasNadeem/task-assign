from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from taskapp.models import Task
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from django.contrib.auth.models import User
from tastypie import fields
from django.db.models import Q

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['id', 'username']
        allowed_methods = ['get']
        authorization = Authorization()

class TaskResource(ModelResource):
    creator = fields.ForeignKey(UserResource, attribute='creator', full=True)
    assigned_to = fields.ToManyField(UserResource, attribute='assigned_to', null=True, full=True)
    class Meta:
        queryset = Task.objects.all()
        resource_name = 'task'
        authentication = ApiKeyAuthentication()
        authorization = Authorization()

    def obj_create(self, bundle, **kwargs):
        assigned_to = bundle.data.get('assigned_to')
        if assigned_to!=[]:
            pass
        else:
            return super(TaskResource, self).obj_create(bundle, creator=bundle.request.user)

    
    def authorized_read_list(self, object_list, bundle):
        # IMPLEMNT - Also the user assigned can read and write 
        return object_list.filter(Q(creator=bundle.request.user) | Q(assigned_to__id=bundle.request.user.id))

