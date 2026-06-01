import json
from urllib.parse import parse_qs

from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        params = parse_qs(self.scope['query_string'].decode())
        token_list = params.get('token', [])

        if not token_list:
            await self.accept()
            await self.close(code=4001)
            return

        try:
            access_token = AccessToken(token_list[0])
            user_id = access_token['user_id']
        except TokenError:
            await self.accept()
            await self.close(code=4001)
            return

        self.group_name = f'notifications_user_{user_id}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def notification_created(self, event):
        await self.send(text_data=json.dumps({
            'event': 'notification.created',
            'payload': event['payload'],
        }))
