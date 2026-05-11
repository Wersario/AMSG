from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


async def broadcast_message(message):
    channel_layer = get_channel_layer()

    await channel_layer.group_send(
        f'chat_{message.chat.id}',
        {
            'type': 'chat.message',
            'message': {
                'sender': message.sender.username,
                'content': message.content,
            }
        }
    )