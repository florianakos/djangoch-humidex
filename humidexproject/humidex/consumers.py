# chat/consumers.py
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
import datetime

from .models import Measurement
from django.db.models import Avg

class HumidexConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'humidex_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        msg_type = text_data_json['msg_type']

        if msg_type == "user_feedback" :
            message = text_data_json['message']
            level = text_data_json['measurement']
            m = Measurement(time=datetime.datetime.now(), room=self.room_name, value=level)
            m.save()

            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'humidex_response',
                    'message': message
                }
            )
        elif msg_type == "periodic_query" :
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'humidex_query_response'
                }
            )


    # Receive message from room group
    def humidex_response(self, event):
        message = event['message']
        avg = Measurement.objects.filter(room=self.room_name).order_by('-id')[:20].aggregate(Avg('value'))

        #print("User feedback received at: ")
        #print(datetime.datetime.now())

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'msg_type': 'user_feedback_response',
            'avg' : avg
        }))

    # Receive message from room group
    def humidex_query_response(self, event):
        avg = Measurement.objects.filter(room=self.room_name).order_by('-id')[:20].aggregate(Avg('value'))
        #print("Automatic query received at: ")
        #print(datetime.datetime.now())

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'msg_type': "periodic_query_response",
            'avg' : avg
        }))
