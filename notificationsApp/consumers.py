import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].username is None:
            self.room_group_name = "Broadcast"
        else:
            self.room_group_name = self.scope["user"].username

        if self.scope["user"].username is None:
            # Reject the connection
            await self.close()
        else:
            # Accept the connection
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            print("group channel name is " + self.room_group_name)

    async def connect_test(self, group_name):
        self.room_group_name = group_name

        if group_name is None:
            # Reject the connection
            await self.close()
        else:
            # Accept the connection
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    # async def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']

    #     # Send message to room group
    #     await self.channel_layer.group_send(
    #         self.room_group_name,
    #         {
    #             'type': 'chat_message',
    #             'message': message
    #         }
    #     )

    # Receive message from room group
    async def channel_message(self, event):
        message = json.loads(event['message'])

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))


class NotificationsConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_group_name = self.scope["user"]

        if self.room_group_name is None:
            # Reject the connection
            await self.close()
        else:
            # Accept the connection
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

    async def connect_test(self, group_name):

        if group_name is None:
            # Reject the connection
            await self.close()
        else:
            # Accept the connection
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            print("group channel name is " + self.room_group_name)


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from room group
    async def channel_message(self, event):
        message = json.loads(event['message'])

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))


