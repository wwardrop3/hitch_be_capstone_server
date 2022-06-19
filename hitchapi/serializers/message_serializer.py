from rest_framework.serializers import ModelSerializer
from hitchapi.models.Message import Message


class MessageSerializer(ModelSerializer):
    
    class Meta:
        model= Message
        fields=("id", "driver_trip", "passenger_trip", "sender", "receiver", "message_text", "is_read", "creation_date")
        depth=1