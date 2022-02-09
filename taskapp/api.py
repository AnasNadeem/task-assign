from traceback import print_tb
from tastypie.resources import ModelResource
from taskapp.models import Task, Profile, FriendRequest
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from django.contrib.auth.models import User
from tastypie import fields
from taskapp.authorization import (
    TaskAuthorization,
    FriendAuthorization, 
    ProfileAuthorization)
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

class ProfileResource(ModelResource):
    user = fields.ForeignKey(UserResource, attribute='user',null=True, full=True)
    friends = fields.ToManyField(UserResource, attribute='friends', null=True,blank=True, full=True)
    class Meta:
        queryset = Profile.objects.all()
        resource_name = 'profile'
        allowed_methods = ['get']
        authentication = ApiKeyAuthentication()
        authorization = ProfileAuthorization()
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

class TaskResource(ModelResource):
    creator = fields.ForeignKey(ProfileResource, attribute='creator',null=True)
    assigned_to = fields.ToManyField(ProfileResource, attribute='assigned_to', null=True,blank=True)
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
        user_prof = Profile.objects.get(user=bundle.request.user)
        assigned_to_data = bundle.data.get('assigned_to', '')
        title_data = bundle.data.get('title', '')
        desc_data = bundle.data.get('description', '')
        tag_data = bundle.data.get('tag', '')
        link_data = bundle.data.get('link', '')
        status_data = bundle.data.get('status', '')
        priority_data = bundle.data.get('priority', '')
        if title_data=='':
            raise BadRequest(f"Include Title.")
        # Checking the assigned_to person is in his friendlist or not - Ofcourse hoga hi cause profile friends s dropdown field hoga ye
        # Creating new task
        new_task = Task()
        new_task.title = title_data
        new_task.description = desc_data
        new_task.tag = tag_data
        new_task.link = link_data
        new_task.status = status_data
        new_task.priority = priority_data
        new_task.creator = user_prof
        new_task.save()
        if assigned_to_data!="":
            assigned_person_data = assigned_to_data.split(',')
            for assigned_person in assigned_person_data:
                assigned_person_prof = Profile.objects.get(user__username=assigned_person)
                new_task.assigned_to.add(assigned_person_prof)
                new_task.save()
        bundle.obj = new_task
        return bundle
