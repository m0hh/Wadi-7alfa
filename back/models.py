from django.db import models
from django.db.models.base import Model

# Create your models here.

class Task(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    dscription = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=200)
    hours = models.IntegerField(default=0)

class SubTask(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    parent = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="childern")