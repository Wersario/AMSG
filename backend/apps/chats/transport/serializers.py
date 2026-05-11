from apps.chats.models import MessageReadModel


class MessageSerializer:

    @staticmethod
    def serialize(message: MessageReadModel):
        return {
            'sender': message.sender_username,
            'content': message.content,
            'created_at': message.created_at.isoformat(),
        }