from apps.chats.models import MessageLog
from apps.chats.projection.projector import project_message


for message in MessageLog.objects.all():
    project_message(message)