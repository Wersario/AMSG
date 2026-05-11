from asgiref.sync import sync_to_async
from apps.chats.models import MessageReadModel


async def project_message(message):
    await sync_to_async(MessageReadModel.objects.create)(
        id=message.id,
        chat_id=message.chat.id,
        sender_username=message.sender.username,
        content=message.content,
        created_at=message.created_at,
    )