from rest_framework.serializers import ModelSerializer
from hitchapi.models.Member import Member


from hitchapi.serializers.user_serializer import UserSerializer


class MemberSerializer(ModelSerializer):
    
    user = UserSerializer()
    
    class Meta:
        
        model = Member
        fields = ("id", "user", "bio", "profile_image_url", "driver_trips", "passenger_trips", "avg_rating", "total_ratings")
        depth= 2