from pyexpat.errors import messages
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from tastypie.models import create_api_key
import random, string

models.signals.post_save.connect(create_api_key, sender=User)

TASK_PRIORITY = [
    ('Lazy', 'Lazy'),
    ('Moderate', 'Moderate'),
    ('Urgent', 'Urgent'),
]

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=12, choices=TASK_PRIORITY, default='Moderate')
    status = models.BooleanField(default=False)
    tag = models.TextField()
    link = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_to = models.ManyToManyField(User, blank=True, related_name='assigned')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # image = models.ImageField(upload_to='image', blank=True)
    friends = models.ManyToManyField(User, blank=True, related_name="profiles")
    created_at = models.DateField(auto_now_add=True, null=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.user.username

STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)

class FriendRequestManager(models.Manager):
    def invitation_recieved(self, receiver):
        qs = FriendRequest.objects.filter(receiver=receiver, status='send')
        return qs 

class FriendRequest(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="senders")
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="receivers")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='send')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = FriendRequestManager()

    def __str__(self):
        return f"{self.sender} - {self.receiver} - {self.status} - {self.updated_at.strftime('%d-%m-%Y')} - {self.created_at.strftime('%d-%m-%Y')}"

class Message(models.Model):
    sender_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="sender_profiles")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender_profile.user.username}-{self.content}"

def gen_unique_code():
  length = 6
  while True:
    code = ''.join(random.choices(string.ascii_uppercase, k=length))
    if Chat.objects.filter(code=code).count()==0:
        break
  return code

class Chat(models.Model):
    code = models.CharField(max_length=6,default=gen_unique_code, blank=True)
    participant = models.ManyToManyField(Profile, blank=True, related_name="participants")
    messages = models.ManyToManyField(Message, blank=True)
    