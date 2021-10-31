from django.urls import path, include
from .views import Login
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login', Login.as_view(), name='login'),
    path('logout', LogoutView.as_view(),{'next_page': 'registration/login.html'}, name='logout'),
]
