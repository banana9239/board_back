from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path("", views.Users.as_view()),
    path("me", views.Me.as_view()),
    path('log-in', views.LogIn.as_view()),
    path('log-out', views.LogOut.as_view()),
    path('github', views.Github.as_view()),
    path('check-username', views.CheckUsername.as_view()),
    
]

