
from rest_framework.serializers import ModelSerializer
from hitchapi.models.Member import Member
from hitchapi.models.PassengerTrip import PassengerTrip
from hitchapi.serializers.member_serializer import MemberSerializer



class PassengerTripSerializer(ModelSerializer):
    
    passenger = MemberSerializer()
    
    class Meta:
        
        model = PassengerTrip
        fields = ("id", "passenger", "origin", "destination", "creation_date", "start_date", "trip_distance", "expected_travel_time", "trip_summary", "completion_date", "driver_trips", "path", "path_points", "recommended_trips")
        depth = 1
        
    
class CreatePassengerTripSerializer(ModelSerializer):

    class Meta:
        
        model = PassengerTrip
        fields = ("id", "passenger", "origin", "destination", "creation_date", "start_date", "trip_distance", "expected_travel_time", "trip_summary", "path", "path_points")
        