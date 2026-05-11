from django.contrib import admin
from django.urls import path
from apps.chats.transport.views import ChatListView, CreateChatView, JoinChatView, ChatDetailView, ExportChatView
from apps.chats.transport.api import ChatHistoryView
from apps.users.views import LoginView, LogoutView
from apps.chats.transport.views import ChatListView, CreateChatView, JoinChatView, ChatDetailView
from apps.users.views import LoginView, LogoutView, RegisterView

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('chats/', ChatListView.as_view(), name='chat_list'),
    path('chats/new/', CreateChatView.as_view(), name='chat_create'),
    path('chats/join/', JoinChatView.as_view(), name='chat_join'),
    path('chats/<int:chat_id>/', ChatDetailView.as_view(), name='chat_detail'),
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view(), name='register'),
    path('api/history/<int:chat_id>/', ChatHistoryView.as_view()),
    path('chats/<int:chat_id>/export/', ExportChatView.as_view(), name='chat_export'),
]

