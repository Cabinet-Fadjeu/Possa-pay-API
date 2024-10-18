
import json
from channels.generic.websocket import AsyncWebsocketConsumer



class PayNotificationConsumer(AsyncWebsocketConsumer):
    
    # Create user connection
    async def connect(self):
        
        self.user = self.scope['user']
        self.group_name = f'user_{self.user.id}'

        # Join room group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()

    # Disconnect user
    async def disconnect(self, code):
        # leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        ) 

    # Receive Notification message from Websocket
    async def receive(self, text_data=None):
        await self.send(text_data=json.dumps({
            'message' : 'Pay Notification received'
        }))

    # Receive message from room group
    async def notify_user(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message' : message
        }))