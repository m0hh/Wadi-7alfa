from django.urls import path
from . import views

urlpatterns = [
    path('task/', views.Clickup, name='endpoint'),
]