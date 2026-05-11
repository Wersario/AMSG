import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from apps.chats.command.commands import SendMessageCommand, EditMessageCommand, DeleteMessageCommand
from apps.chats.command.handlers import SendMessageHandler, EditMessageHandler, DeleteMessageHandler


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.group_name = f'chat_{self.chat_id}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        payload = json.loads(text_data)
        action = payload.get('action', 'send')
        user_id = self.scope['user'].id

        if action == 'send':
            command = SendMessageCommand(
                chat_id=self.chat_id,
                sender_id=user_id,
                content=payload['content'],
            )
            message = await SendMessageHandler.handle(command)
            await self.channel_layer.group_send(self.group_name, {
                'type': 'chat.message',
                'message': {
                    'action': 'send',
                    'id': message.id,
                    'sender': message.sender.username,
                    'content': message.content,
                }
            })

        elif action == 'edit':
            command = EditMessageCommand(
                message_id=payload['message_id'],
                user_id=user_id,
                new_content=payload['content'],
            )
            try:
                message = await sync_to_async(EditMessageHandler.handle)(command)
                await self.channel_layer.group_send(self.group_name, {
                    'type': 'chat.message',
                    'message': {
                        'action': 'edit',
                        'id': message.id,
                        'content': message.content,
                    }
                })
            except ValueError as e:
                await self.send(text_data=json.dumps({'error': str(e)}))

        elif action == 'delete':
            command = DeleteMessageCommand(
                message_id=payload['message_id'],
                user_id=user_id,
                chat_id=self.chat_id,
            )
            try:
                message = await sync_to_async(DeleteMessageHandler.handle)(command)
                await self.channel_layer.group_send(self.group_name, {
                    'type': 'chat.message',
                    'message': {
                        'action': 'delete',
                        'id': message.id,
                    }
                })
            except ValueError as e:
                await self.send(text_data=json.dumps({'error': str(e)}))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['message']))