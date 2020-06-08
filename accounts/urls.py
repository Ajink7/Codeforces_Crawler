from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('signup/',SignUpView.as_view(),name='signup'),
    path('login/',auth_views.LoginView.as_view(template_name = 'accounts/login.html' ),name= 'login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('profile/<str:username>/',get_profile,name = 'profile'),
    path('create_profile/',CreateProfileView.as_view(),name = 'create_profile'),
    path('update_profile/',UpdateProfileView.as_view(),name = 'update_profile'),
    path('profile/<str:username>/send_friend_request',send_friend_request,name='send_friend_request'),
    path('profile/<str:username>/cancel_friend_request',cancel_friend_request,name = 'cancel_friend_request'),
    path('profile/<str:username>/accept_friend_request',accept_friend_request,name = 'accept_friend_request'),
    path('profile/<str:username>/delete_friend_request',delete_friend_request,name = 'delete_friend_request'),
    path('profile/<str:username>/remove_friend',remove_friend,name = 'remove_friend'),
    path('search_users/',SearchUsers.as_view(),name = 'search_users')
]
