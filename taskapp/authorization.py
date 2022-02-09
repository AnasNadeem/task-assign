from tastypie.authorization import Authorization
from django.db.models import Q
from taskapp.models import Profile

class TaskAuthorization(Authorization):
    def get_profile(self, bundle):
        return Profile.objects.get(user=bundle.request.user)

    def read_list(self, object_list, bundle):
        profile = self.get_profile(bundle)
        return object_list.filter(Q(creator=profile) | Q(assigned_to__id=profile.id))

    def read_detail(self, object_list, bundle):
        profile = self.get_profile(bundle)
        if object_list.filter(Q(creator=profile) | Q(assigned_to__id=profile.id)):
            return True
        else:
            return False

    def update_list(self, object_list, bundle):
        profile = self.get_profile(bundle)
        return object_list.filter(Q(creator=profile) | Q(assigned_to__id=profile.id))

    def update_detail(self, object_list, bundle):
        profile = self.get_profile(bundle)
        if object_list.filter(Q(creator=profile) | Q(assigned_to__id=profile.id)):
            return True
        else:
            return False

    def delete_list(self, object_list, bundle):
        profile = self.get_profile(bundle)
        return object_list.filter(Q(creator=profile) | Q(assigned_to__id=profile.id))

    def delete_detail(self, object_list, bundle):
        profile = self.get_profile(bundle)
        if object_list.filter(Q(creator=profile) | Q(assigned_to__id=profile.id)):
            return True
        else:
            return False

class FriendAuthorization(Authorization):
    def get_profile(self, bundle):
        return Profile.objects.get(user=bundle.request.user)

    def read_list(self, object_list, bundle):
        profile = self.get_profile(bundle)
        return object_list.filter(Q(sender=profile) | Q(receiver=profile))

    def read_detail(self, object_list, bundle):
        profile = self.get_profile(bundle)
        if object_list.filter(Q(sender=profile) | Q(receiver=profile)):
            return True
        else:
            return False

    def update_list(self, object_list, bundle):
        profile = self.get_profile(bundle)
        return object_list.filter(Q(sender=profile) | Q(receiver=profile))

    def update_detail(self, object_list, bundle):
        profile = self.get_profile(bundle)
        if object_list.filter(Q(sender=profile) | Q(receiver=profile)):
            return True
        else:
            return False

    def delete_list(self, object_list, bundle):
        profile = self.get_profile(bundle)
        return object_list.filter(Q(sender=profile) | Q(receiver=profile))

    def delete_detail(self, object_list, bundle):
        profile = self.get_profile(bundle)
        if object_list.filter(Q(sender=profile) | Q(receiver=profile)):
            return True
        else:
            return False

class ProfileAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(user__username=bundle.request.user)
