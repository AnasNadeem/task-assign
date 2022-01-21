from django.db import models
from django.contrib.auth.models import User

TASK_STATUS = [
    ('Moderate', 'Moderate'),
    ('Urgent', 'Urgent'),
]

TASK_PROGRESS = [
    ('Pending', 'Pending'),
    ('Working', 'Working'),
    ('Completed', 'Completed'),
]

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=8, choices=TASK_STATUS, default='Moderate')
    progress = models.CharField(max_length=12, choices=TASK_PROGRESS, default='Pending')
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_to = models.ManyToManyField(User, blank=True, related_name='assigned')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title