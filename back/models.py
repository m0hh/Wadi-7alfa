from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey

# Create your models here.




class UserInfo(models.Model):
    api_pk = models.CharField(max_length=200, default='0')
    team_id = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='info')
    name = models.CharField(max_length=200, default='Guest')
    site_id = models.IntegerField()
    webhook_id = models.CharField(max_length=200, default='0')


class Space(models.Model):
    id = models.CharField(max_length=400, primary_key=True)
    name = models.CharField(max_length=300, blank=True, null=True)
    private = models.BooleanField()
    creator = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name="spaces")

class List(models.Model):
    id = models.CharField(max_length=300, primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name="lists")

class Task(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    dscription = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=200)
    hours = models.IntegerField(default=0)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='tasks', default='0')
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    time_estimate = models.FloatField(default=0, blank=True, null=True)
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name="tasks", null=True, blank=True)

class SubTask(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    parent = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="childern")
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='sub_tasks', default='0')


class Assignees(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="assingees")
    worker = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name="assignments")


class TimeTaskHistory(models.Model):
    time_id = models.CharField(max_length=400, default="0")
    started = models.DateTimeField(null=True,blank=True)
    ended = models.DateTimeField(null = True, blank= True)
    time = models.CharField(max_length=300, null=True, blank=True)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name="times")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="times")



