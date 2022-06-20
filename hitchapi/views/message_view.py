
from ast import Pass
import datetime
from sqlite3 import Date
from xmlrpc.client import DateTime
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
import polyline
from geopy import distance
from geopy.distance import great_circle


from hitchapi.models.DriverTrip import DriverTrip
from hitchapi.models.Member import Member
from hitchapi.models.Message import Message
from hitchapi.models.PassengerTrip import PassengerTrip
from hitchapi.serializers.message_serializer import MessageSerializer
from hitchapi.serializers.passenger_trip_serializer import PassengerTripSerializer 

class MessageView(ViewSet):
    
    def retrieve(self, request, pk):
        message = Message.objects.get(pk = pk)
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        
        sender = Member.objects.get(user = request.auth.user)
        receiver = Member.objects.get(pk = request.data['receiver'])
        driver_trip = DriverTrip.objects.get(pk = request.data['driver_trip'])
        passenger_trip = PassengerTrip.objects.get(pk = request.data['passenger_trip'])
    
        request.data['creation_date'] = datetime.datetime.now()
        message = MessageSerializer(data = request.data)
        message.is_valid(raise_exception=True)
        message.save(sender = sender, receiver=receiver, driver_trip=driver_trip, passenger_trip = passenger_trip)
        
        return Response("Message Sent", status = status.HTTP_201_CREATED)
    
    
    
    
    
    @action(methods=['get'], detail=False)    
    def get_all_member_messages(self, request):
        member = Member.objects.get(user = request.auth.user)
        messages = Message.objects.filter(sender = member) | Message.objects.filter(receiver = member)
        serializer = MessageSerializer(messages, many = True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(methods=['get'], detail=True)    
    def get_driver_trip_messages(self, request, pk):
        
        driver_trip = DriverTrip.objects.get(pk = pk)
    
        messages = Message.objects.filter(driver_trip = driver_trip)
        
        serializer = MessageSerializer(messages, many = True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(methods=['get'], detail=True)    
    def get_passenger_trip_messages(self, request, pk):
        
        passenger_trip = PassengerTrip.objects.get(pk = pk)
    
        messages = Message.objects.filter(passenger_trip = passenger_trip)
        
        serializer = MessageSerializer(messages, many = True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)