from rest_framework.serializers import ModelSerializer
from hitchapi.models.Member import Member


from hitchapi.serializers.user_serializer import UserSerializer


class MemberSerializer(ModelSerializer):
    
    user = UserSerializer()
    
    class Meta:
        
        model = Member
        fields = ("user", "bio", "profile_image_url", "driver_trips", "passenger_trips")
        depth= 1