from django.urls import path
from .views import tasks, subtasks,index, sync

urlpatterns = [
    path('tasks/', tasks, name='tasksclient'),
    path('subtasks/', subtasks, name='subtasksclient'),
    path('sync/', sync, name = 'sync'),
    path('', index, name='home')
]
