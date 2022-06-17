from pyexpat import model
from rest_framework.serializers import ModelSerializer
from hitchapi.models.DriverTripRating import DriverTripRating

from hitchapi.serializers.driver_trip_serializer import DriverTripSerializer
from hitchapi.serializers.passenger_trip_serializer import PassengerTripSerializer

class DriverTripRatingSerializer(ModelSerializer):

    
    class Meta:
        model = DriverTripRating
        fields = ("id", "driver_trip", "passenger_trip", "rating", "review")
        depth = 1
    
class CreateDriverTripRatingSerializer(ModelSerializer):

    
    class Meta:
        model = DriverTripRating
        fields = ("driver_trip", "passenger_trip", "rating", "review")
        depth = 1
    