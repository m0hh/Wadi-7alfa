from django.urls import path
from .views import tasks, subtasks

urlpatterns = [
    path('tasks/', tasks, name='tasksclient'),
    path('subtasks/', subtasks, name='subtasksclient'),
]
