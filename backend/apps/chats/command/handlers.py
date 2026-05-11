from apps.users.models import User
from apps.chats.infrastructure.async_queue import fire_and_forget
from apps.chats.projection.projector import project_message
from apps.chats.infrastructure.broadcaster import broadcast_message
from asgiref.sync import sync_to_async
from apps.chats.models import MessageLog, MessageReadModel, Chat


class SendMessageHandler:

    @staticmethod
    async def handle(command):
        chat = await sync_to_async(Chat.objects.get)(id=command.chat_id)
        sender = await sync_to_async(User.objects.get)(id=command.sender_id)

        message = await sync_to_async(MessageLog.objects.create)(
            chat=chat,
            sender=sender,
            content=command.content,
        )

        fire_and_forget(project_message(message))
        fire_and_forget(broadcast_message(message))

        return message


class JoinChatHandler:

    @staticmethod
    def handle(command):
        chat = Chat.objects.filter(invite_code=command.invite_code).first()
        if chat is None:
            raise ValueError('Чат с таким кодом не найден.')
        user = User.objects.get(id=command.user_id)
        chat.participants.add(user)
        return chat


class CreateChatHandler:

    @staticmethod
    def handle(command):
        creator = User.objects.get(id=command.creator_id)
        chat = Chat.objects.create(title=command.title, creator=creator)
        chat.participants.add(creator)
        return chat


class EditMessageHandler:

    @staticmethod
    def handle(command):
        message = MessageLog.objects.get(id=command.message_id)

        if message.sender_id != command.user_id:
            raise ValueError('Нельзя редактировать чужое сообщение.')

        message.content = command.new_content
        message.is_edited = True
        message.save()

        MessageReadModel.objects.filter(id=message.id).update(content=command.new_content, is_edited=True)

        return message


class DeleteMessageHandler:

    @staticmethod
    def handle(command):
        from apps.users.models import User as UserModel
        message = MessageLog.objects.get(id=command.message_id)
        user = UserModel.objects.get(id=command.user_id)
        chat = Chat.objects.get(id=command.chat_id)

        is_owner = message.sender_id == command.user_id
        is_chat_creator = chat.creator_id == command.user_id
        is_superuser = user.is_superuser

        if not (is_owner or is_chat_creator or is_superuser):
            raise ValueError('Недостаточно прав для удаления.')

        message.is_deleted = True
        message.content = ''
        message.save()

        MessageReadModel.objects.filter(id=message.id).update(is_deleted=True, content='')
        
        return message
