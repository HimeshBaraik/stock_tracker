# chat/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class StockConsumer(WebsocketConsumer):
    def connect(self):
        # Join stock updates group
        self.group_name = "stock_updates"
        
        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave stock updates group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )

    # Receive message from WebSocket (currently not processing client input)
    def receive(self, text_data):
        # Client input will be implemented later
        # For now, we only broadcast stock data from Celery Beat
        pass

    # Receive stock data update from Celery task via channel layer
    def stock_update(self, event):
        """
        Handler for stock data updates from Celery task
        """
        stock_data = event["stock_data"]
        
        # Send stock data to WebSocket client
        self.send(text_data=json.dumps({
            "type": "stock_update",
            "data": stock_data
        }))