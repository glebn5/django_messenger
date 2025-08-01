from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .forms import *
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.db.models import Q
from django.contrib.auth import get_user_model

# Create your views here.
    
def chat_page(request):
    user = request.user
    private_chats = PrivateChat.objects.filter(Q(user_1=user) | Q(user_2=user))
    group_chats = RoomName.objects.filter(participant=user)
    
    return render(request, 'chat/chatPage.html', {
        'private_chats': private_chats,
        'group_chats': group_chats,
    })      


def room(request, room_name):
    if not request.user.is_authenticated:
        return redirect("login_user")

    room, _ = RoomName.objects.get_or_create(name=room_name)
    messages = GroupMessage.objects.filter(room_name=room).order_by('timestamp')
    participants = room.participant.all()

    context = {
        "room_name": room.name,
        "messages": messages,
        "participants": participants,
        }
    return render(request, 'chat/roomPage.html', context=context)


class Register(View):
    template_name = 'chat/register.html'

    def get(self, request):
        context = {'form': SignUpForm()}
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            user_id = self.request.user.id
            return redirect('main_page')
        context={'form':form}
        return render(request, self.template_name, context)
    
class LogView(LoginView):
    template_name = 'profile/login.html'
    fields = ['email', 'password']
    redirect_authenticated_user = True
    
    def get_success_url(self):
        user_id = self.request.user.id
        return reverse_lazy('main_page')
    
def main_page(request):
    if not request.user.is_authenticated:
        return redirect("login_user")
    render(request, 'chat/mainPage.html',)


def private_chat(request, chat_id):
    if not request.user.is_authenticated:
        return redirect("login_user")
    
    chat = get_object_or_404(PrivateChat, id=chat_id)

    
    if request.user not in chat.participants():
        return HttpResponseForbidden("You are not allowed to access this chat.")
    messages = PrivateMessage.objects.filter(private_chat=chat).order_by('timestamp')

    context = {
        'chat': chat,
        'messages': messages,
        'other_user': chat.user_2 if chat.user_1 == request.user else chat.user_1
    }
    return render(request, 'chat/private_chat.html', context)


def add_participant_in_group_view(request, room_name: str):
    room, _ = RoomName.objects.get_or_create(name=room_name)
    room.participant.add(request.user)
    return redirect('room', room_name=room.name)

User = get_user_model()

def profile_view(request, username):
    if not request.user.is_authenticated:
        return redirect("login_user")

    user_profile = get_object_or_404(User, username=username)

    # Если это НЕ текущий пользователь, проверить или создать приватный чат
    chat = None
    if user_profile != request.user:
        u1, u2 = sorted([request.user, user_profile], key=lambda u: u.id)
        chat, created = PrivateChat.objects.get_or_create(user_1=u1, user_2=u2)

    context = {
        'target_user': user_profile,
        'chat': chat,
    }
    return render(request, 'chat/target_profile.html', context)