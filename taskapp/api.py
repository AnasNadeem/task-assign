from tastypie.resources import ModelResource
from taskapp.models import Task, Profile, FriendRequest
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from django.contrib.auth.models import User
from tastypie import fields
from taskapp.authorization import TaskAuthorization, FriendAuthorization
from tastypie.exceptions import BadRequest
from tastypie.constants import ALL, ALL_WITH_RELATIONS

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['id', 'username']
        allowed_methods = ['get']
        authorization = Authorization()
        filtering = {
            "username":('exact', 'startswith')
        }

class TaskResource(ModelResource):
    creator = fields.ForeignKey(UserResource, attribute='creator',null=True, full=True)
    assigned_to = fields.ToManyField(UserResource, attribute='assigned_to', null=True,blank=True, full=True)
    class Meta:
        queryset = Task.objects.all()
        resource_name = 'task'
        authentication = ApiKeyAuthentication()
        authorization = TaskAuthorization()
        always_return_data = True

    def obj_create(self, bundle, **kwargs):
        bundle = self.full_hydrate(bundle)    
        return super(TaskResource, self).obj_create(bundle, creator=bundle.request.user) 

class ProfileResource(ModelResource):
    user = fields.ForeignKey(UserResource, attribute='user',null=True, full=True)
    class Meta:
        queryset = Profile.objects.all()
        resource_name = 'profile'
        allowed_methods = ['get']
        authorization = Authorization()
        filtering = {
            "user":ALL_WITH_RELATIONS
        }

class FriendResource(ModelResource):
    sender = fields.ForeignKey(ProfileResource, attribute='sender',null=True, full=True)
    receiver = fields.ForeignKey(ProfileResource, attribute='receiver',null=True, full=True)
    class Meta:
        queryset = FriendRequest.objects.all()
        resource_name = 'friend'
        authentication = ApiKeyAuthentication()
        authorization = FriendAuthorization()
        always_return_data = True

    def obj_create(self, bundle, **kwargs):
        bund_data = self.full_hydrate(bundle)    
        user_prof = Profile.objects.get(user=bundle.request.user)
        return super(FriendResource, self).obj_create(bund_data, sender=user_prof)