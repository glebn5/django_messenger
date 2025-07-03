from django.urls import path, include
from django.contrib.auth import views
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path("", ChatsPage.as_view(), name = "chat_page"),
    path("<str:room_name>/", room, name = 'room'),
    path("auth/login/", views.LoginView.as_view(template_name="chat/login.html"), name="login_user"),
    path("logout/", LogoutView.as_view(), name = "logout_user"),
    path("main/", main_page, name = 'main_page'),
    path("auth/register/", Register.as_view(), name = 'register'),

    path('profile/<str:target_username>/', target_profile_view, name='target_profile'),
    path('chat/<int:chat_id>/', private_chat, name='private_chat'),



]