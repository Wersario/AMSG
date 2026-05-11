from django.http import JsonResponse
from django.views import View

from apps.chats.query.queries import GetHistoryQuery
from apps.chats.query.handlers import GetHistoryHandler


class ChatHistoryView(View):

    def get(self, request, chat_id):
        query = GetHistoryQuery(chat_id=chat_id)
        messages = GetHistoryHandler.handle(query)

        return JsonResponse({
            'messages': [m.__dict__ for m in messages]
        })