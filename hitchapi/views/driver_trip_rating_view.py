
import datetime
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response

from hitchapi.models.DriverTrip import DriverTrip
from hitchapi.models.Member import Member
from hitchapi.models.Message import Message
from hitchapi.models.PassengerTrip import PassengerTrip
from hitchapi.serializers.driver_trip_rating_serializer import CreateDriverTripRatingSerializer, DriverTripRatingSerializer
from hitchapi.serializers.driver_trip_serializer import CreateDriverTripSerializer, DriverTripSerializer, UpdateDriverTripSerializer
from hitchapi.serializers.message_serializer import MessageSerializer
from hitchapi.serializers.passenger_trip_serializer import PassengerTripSerializer 

class DriverTripRatingView(ViewSet):    
    
    def create(self, request):
        
        driver_trip = DriverTrip.objects.get(pk = request.data['driver_trip'])
        
        passenger_trip = PassengerTrip.objects.get(pk = request.data['passenger_trip'])
        
  
        
       
        driver_trip_rating = CreateDriverTripRatingSerializer(data = request.data)
        driver_trip_rating.is_valid(raise_exception=True)
        driver_trip_rating.save(driver_trip=driver_trip, passenger_trip=passenger_trip)
        
    
        new_message = Message.objects.create(
            driver_trip = driver_trip,
            passenger_trip=passenger_trip,
            sender = passenger_trip.passenger,
            receiver = driver_trip.driver,
            creation_date = datetime.datetime.now(),
            message_text = passenger_trip.passenger.user.first_name + " " + passenger_trip.passenger.user.last_name + " gave a review: " + request.data['review'] + ". Rating: " + str(request.data['rating']) + "/5",
            is_read = False
            
        )
        
        
        return Response(None, status=status.HTTP_201_CREATED)