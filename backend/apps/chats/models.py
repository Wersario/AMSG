from django.db import models
from django.conf import settings
import secrets
import string


def generate_invite_code():
    alphabet = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(8))


class Chat(models.Model):
    title = models.CharField(max_length=255)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='created_chats')
    invite_code = models.CharField(max_length=16, unique=True, default=generate_invite_code)
    created_at = models.DateTimeField(auto_now_add=True)


class MessageLog(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class MessageReadModel(models.Model):
    id = models.IntegerField(primary_key=True)
    chat_id = models.IntegerField()
    sender_username = models.CharField(max_length=255)
    content = models.TextField()
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField()