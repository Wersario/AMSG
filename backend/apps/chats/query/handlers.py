from apps.chats.models import MessageReadModel
from .read_models import MessageDTO


class GetHistoryHandler:

    @staticmethod
    def handle(query):
        messages = MessageReadModel.objects.filter(
            chat_id=query.chat_id
        ).order_by('created_at')

        return [
            MessageDTO(
                sender=msg.sender_username,
                content=msg.content,
                created_at=msg.created_at,
            )
            for msg in messages
        ]