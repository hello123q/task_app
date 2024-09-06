# tasks/models.py
from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255, null=False)
    due_date = models.DateField(null=False, blank=False)
    category = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.title
