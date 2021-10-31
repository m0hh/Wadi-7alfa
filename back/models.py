from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserInfo(models.Model):
    api_pk = models.CharField(max_length=200, default='0')
    team_id = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='info')
    name = models.CharField(max_length=200, default='Guest')
    site_id = models.IntegerField()
    webhook_id = models.CharField(max_length=200, default='0')

class Task(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    dscription = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=200)
    hours = models.IntegerField(default=0)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='tasks', default='0')

class SubTask(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    parent = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="childern")
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='sub_tasks', default='0')

