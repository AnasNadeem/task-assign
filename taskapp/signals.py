from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, FriendRequest, Chat

@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=FriendRequest)
def post_save_add_to_friends(sender, instance, created, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.receiver
    if instance.status== "accepted":
        sender_.friends.add(receiver_.user)
        receiver_.friends.add(sender_.user)
        sender_.save()
        receiver_.save()
        # Create Chat with sender and receiver as its participants
        chat = Chat()
        chat.save()
        chat.participant.add(sender_)
        chat.save()
        chat.participant.add(receiver_)
        chat.save()
         
@receiver(pre_delete, sender=FriendRequest)
def pre_delete_remove_from_friends(sender, instance, **kwargs):
    sender = instance.sender
    receiver = instance.receiver
    sender.friends.remove(receiver.user)
    receiver.friends.remove(sender.user)

    sender.save()
    receiver.save()