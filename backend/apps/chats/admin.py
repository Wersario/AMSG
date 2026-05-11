from django.contrib import admin
from .models import Chat, MessageLog, MessageReadModel

admin.site.register(Chat)
admin.site.register(MessageLog)
admin.site.register(MessageReadModel)