from tastypie.resources import ModelResource
from taskapp.models import Task, Profile, FriendRequest, Chat
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from django.contrib.auth.models import User
from tastypie import fields
from taskapp.authorization import (
    TaskAuthorization,
    FriendAuthorization, 
    ProfileAuthorization,
    ChatAuthorization)
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.exceptions import BadRequest
from django.db.models import Q

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['id', 'username']
        allowed_methods = ['get']
        authentication = ApiKeyAuthentication()
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
        filtering = {
            'creator':ALL_WITH_RELATIONS,
            'assigned_to':ALL_WITH_RELATIONS,
            'created_at': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }

    def obj_create(self, bundle, **kwargs):
        bundle = self.full_hydrate(bundle)    
        return super(TaskResource, self).obj_create(bundle, creator=bundle.request.user) 

class ProfileResource(ModelResource):
    user = fields.ForeignKey(UserResource, attribute='user',null=True, full=True)
    friends = fields.ToManyField(UserResource, attribute='friends', null=True,blank=True, full=True)
    class Meta:
        queryset = Profile.objects.all()
        resource_name = 'profile'
        allowed_methods = ['get']
        authentication = ApiKeyAuthentication()
        authorization = ProfileAuthorization()

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
        user_prof = Profile.objects.get(user=bundle.request.user)
        receiver_data = bundle.data.get('receiver', '')
        if receiver_data=='':
            raise BadRequest(f"Include receiver.")
        receiver_prof = Profile.objects.filter(user__username=receiver_data)
        if receiver_prof:
            # Check if the FriendRequest exist or not 
            frnd_req = FriendRequest.objects.filter((Q(sender=user_prof) & Q(receiver=receiver_prof[0])) | (Q(sender=receiver_prof[0]) & Q(receiver=user_prof)))
            if frnd_req:
                raise BadRequest(f"Already {frnd_req[0].status}")
            new_frnd_req = FriendRequest.objects.create(sender=user_prof, receiver=receiver_prof[0])
            bundle.obj = new_frnd_req
            return bundle
        else:
            raise BadRequest(f"Invalid username.")

class ChatResource(ModelResource):
    # participant = fields.ToManyField(ProfileResource, attribute='participants', null=True,blank=True, full=True)
    class Meta:
        queryset = Chat.objects.all()
        resource_name = 'chat'
        allowed_methods = ['get']
        authentication = ApiKeyAuthentication()
        authorization = ChatAuthorization()