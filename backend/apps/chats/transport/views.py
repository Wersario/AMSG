from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.http import HttpResponse
from apps.chats.models import Chat, MessageReadModel
from apps.chats.command.commands import CreateChatCommand, JoinChatCommand
from apps.chats.command.handlers import CreateChatHandler, JoinChatHandler
from django.utils import timezone


class ChatListView(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        chats = Chat.objects.filter(participants=request.user).order_by('-created_at')
        return render(request, 'chats/chat_list.html', {'chats': chats})


class CreateChatView(LoginRequiredMixin, View):
    login_url = '/'

    def post(self, request):
        title = request.POST.get('title', '').strip()
        if not title:
            chats = Chat.objects.filter(participants=request.user).order_by('-created_at')
            return render(request, 'chats/chat_list.html', {
                'chats': chats,
                'error_create': 'Введите название чата.',
            })
        command = CreateChatCommand(title=title, creator_id=request.user.id)
        chat = CreateChatHandler.handle(command)
        return redirect('chat_detail', chat_id=chat.id)


class JoinChatView(LoginRequiredMixin, View):
    login_url = '/'

    def post(self, request):
        invite_code = request.POST.get('invite_code', '').strip().upper()
        try:
            command = JoinChatCommand(invite_code=invite_code, user_id=request.user.id)
            chat = JoinChatHandler.handle(command)
            return redirect('chat_detail', chat_id=chat.id)
        except ValueError as e:
            chats = Chat.objects.filter(participants=request.user).order_by('-created_at')
            return render(request, 'chats/chat_list.html', {
                'chats': chats,
                'error_join': str(e),
            })


class ChatDetailView(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request, chat_id):
        chat = get_object_or_404(Chat, id=chat_id, participants=request.user)
        messages = MessageReadModel.objects.filter(chat_id=chat_id).order_by('created_at')
        user_chats = Chat.objects.filter(participants=request.user).order_by('-created_at')
        return render(request, 'chats/chat_detail.html', {
            'chat': chat,
            'messages': messages,
            'user_chats': user_chats,
        })


class ExportChatView(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request, chat_id):
        chat = get_object_or_404(Chat, id=chat_id, participants=request.user)
        messages = MessageReadModel.objects.filter(chat_id=chat_id).order_by('created_at')

        data = {
            'chat': chat.title,
            'invite_code': chat.invite_code,
            'exported_by': request.user.username,
            'messages': [
                {
                    'sender': msg.sender_username,
                    'content': msg.content,
                    'created_at': timezone.localtime(msg.created_at).strftime('%Y-%m-%d %H:%M:%S'),
                }
                for msg in messages
            ]
        }

        response = HttpResponse(
            json.dumps(data, ensure_ascii=False, indent=2),
            content_type='application/json',
        )
        response['Content-Disposition'] = f'attachment; filename="chat_{chat_id}.json"'
        return response