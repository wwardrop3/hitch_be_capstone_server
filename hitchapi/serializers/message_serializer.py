from rest_framework.serializers import ModelSerializer
from hitchapi.models.Message import Message
from hitchapi.serializers.member_serializer import MemberSerializer


class MessageSerializer(ModelSerializer):
    
    sender = MemberSerializer()
    receiver = MemberSerializer()
    
    class Meta:
        model= Message
        fields=("id", "driver_trip", "passenger_trip", "sender", "receiver", "message_text", "is_read", "creation_date")
        depth=1
        
class CreateMessageSerializer(ModelSerializer):
    
    
    class Meta:
        model= Message
        fields=("id", "driver_trip", "passenger_trip", "sender", "receiver", "message_text", "is_read", "creation_date")
        