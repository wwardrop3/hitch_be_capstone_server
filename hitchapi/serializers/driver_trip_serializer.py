from rest_framework.serializers import ModelSerializer
from hitchapi.models.Member import Member

from hitchapi.models.DriverTrip import DriverTrip
from hitchapi.serializers.member_serializer import MemberSerializer



class DriverTripSerializer(ModelSerializer):
    
    driver = MemberSerializer()
    
    class Meta:
        
        model = DriverTrip
        fields = ("id", "driver", "tags", "creation_date", "start_date", "completion_date", "detour_radius", "trip_distance", "expected_travel_time", "trip_summary", "seats", "completed", "destination", "origin", "passenger_trips", "path", "path_points", "is_user", "is_signed_up", "is_assigned", "origin_place", "destination_place")
        depth=2
        
    
class CreateDriverTripSerializer(ModelSerializer):

    driver = Member()
    
    class Meta:
        
        
        model = DriverTrip
        fields = ("id", "driver", "tags", "creation_date", "start_date", "detour_radius", "trip_distance", "expected_travel_time", "trip_summary", "seats", "completed", "destination", "origin", "path", "path_points", "origin_place", "destination_place")
        
        
class UpdateDriverTripSerializer(ModelSerializer):

    driver = Member()
    
    class Meta:
        
        
        model = DriverTrip
        fields = ("id", "tags", "creation_date", "start_date", "detour_radius", "trip_distance", "expected_travel_time", "trip_summary", "seats", "completed", "origin_place", "destination_place")
        
        
