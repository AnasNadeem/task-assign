import json
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
    creator = fields.ForeignKey(UserResource, attribute='creator',null=True, full=True)
    assigned_to = fields.ToManyField(UserResource, attribute='assigned_to', null=True,blank=True, full=True)
    class Meta:
        queryset = Task.objects.all()
        resource_name = 'task'
        authentication = ApiKeyAuthentication()
        authorization = Authorization()

    # def hydrate_assigned_to(self, bundle, **kwargs):
    #     if bundle.data['assigned_to']:
    #         # new_list = []
    #         for assigned_data in bundle.data['assigned_to']:
    #             user = User.objects.filter(username=assigned_data)
    #             try:
    #                 new_dict = {
    #                     "id":user[0].id,
    #                     "username":assigned_data
    #                 }
    #                 # new_list.append(json.dumps(new_dict))
    #                 # new_list.append(new_dict)
    #             except:
    #                 pass
    #             # if user and user[0].id not in new_list:
    #             #     new_list.append(user[0].id)
    #         # bundle.data['assigned_to'] = json.dumps(new_list)
    #     return bundle

    def obj_create(self, bundle, **kwargs):
        bundle = self.full_hydrate(bundle)    
        return super(TaskResource, self).obj_create(bundle, creator=bundle.request.user)

    
    def authorized_read_list(self, object_list, bundle):
        # IMPLEMNT - Also the user assigned can read and write 
        return object_list.filter(Q(creator=bundle.request.user) | Q(assigned_to__id=bundle.request.user.id))

