from tastypie.authorization import Authorization
from django.db.models import Q

class TaskAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(Q(creator=bundle.request.user) | Q(assigned_to__id=bundle.request.user.id))

    def read_detail(self, object_list, bundle):
        if object_list.filter(Q(creator=bundle.request.user) | Q(assigned_to__id=bundle.request.user.id)):
            return True
        else:
            return False

    def update_list(self, object_list, bundle):
        return object_list.filter(Q(creator=bundle.request.user) | Q(assigned_to__id=bundle.request.user.id))

    def update_detail(self, object_list, bundle):
        if object_list.filter(Q(creator=bundle.request.user) | Q(assigned_to__id=bundle.request.user.id)):
            return True
        else:
            return False

    def delete_list(self, object_list, bundle):
        return object_list.filter(Q(creator=bundle.request.user) | Q(assigned_to__id=bundle.request.user.id))

    def delete_detail(self, object_list, bundle):
        if object_list.filter(Q(creator=bundle.request.user) | Q(assigned_to__id=bundle.request.user.id)):
            return True
        else:
            return False