from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from hitchapi.models.DriverTrip import DriverTrip
from hitchapi.models.DriverTripRating import DriverTripRating

from hitchapi.models.Member import Member
from hitchapi.models.PassengerTrip import PassengerTrip
from hitchapi.serializers import driver_trip_serializer
from hitchapi.serializers.driver_trip_serializer import DriverTripSerializer
from hitchapi.serializers.member_serializer import MemberSerializer
from hitchapi.serializers.passenger_trip_serializer import PassengerTripSerializer
from hitchapi.views.passenger_trip_view import PassengerTripView


class MemberView(ViewSet):
    
    def list(self, request):

        members = Member.objects.all()
        
        serializer = MemberSerializer(members, many = True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk):
        
        member = Member.objects.get(user = request.auth.user)
        
        passenger_trips = PassengerTrip.objects.filter(passenger = member)
        passenger_trips_serializer = PassengerTripSerializer(passenger_trips, many = True)
        
        driver_trips = DriverTrip.objects.filter(driver = member)
        
        driver_trips_serializer = DriverTripSerializer(driver_trips, many = True)
        
        avg_rating = 0
        total_ratings = 0
        
        for driver_trip in driver_trips:
            ratings = DriverTripRating.objects.filter(driver_trip = driver_trip)
            
            for rating in ratings:
                avg_rating += rating.rating
                total_ratings += 1
        
        try:
            member.avg_rating = avg_rating / total_ratings
            member.total_ratings = total_ratings
        except:
            pass    
        

        
        

        
        member.passenger_trips = passenger_trips_serializer.data
        member.driver_trips = driver_trips_serializer.data
        
        
        
        
        serializer = MemberSerializer(member)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def destroy(self, request, pk):
        member = Member.objects.get(pk = pk)
        
        member.delete()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    