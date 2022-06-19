from ast import Pass
from crypt import methods
import datetime

from os import stat
from re import M
from sqlite3 import Date
from xmlrpc.client import DateTime
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from hitchapi.models.Location import Location
from rest_framework.decorators import action
import polyline
from geopy import distance
from geopy.distance import great_circle


from hitchapi.models.PassengerTrip import PassengerTrip
from hitchapi.models.Member import Member
from hitchapi.models.PassengerTrip import PassengerTrip
from hitchapi.serializers.passenger_trip_serializer import CreatePassengerTripSerializer, PassengerTripSerializer, UpdatePassengerTripSerializer 

class PassengerTripView(ViewSet):
    
    def list(self, request):
        """get all trips from a user"""
        passenger_trips = PassengerTrip.objects.all()
        
        try:
            
            
            lat = request.query_params.get('lat', None)
            lng = request.query_params.get('lng', None)
            
            
                
            
            
            
            if lat is not None and lng is not None:
                # game_type will be the id of the gametype being queried 
                
            
                filtered_trips = []
                
                for trip in passenger_trips:
                    
                    if trip.passenger.user == request.auth.user:
                        trip.is_user = True
                    else:
                        trip.is_user = False
                        
                        if len(trip.passenger_trips.all()) == 0:
                            trip.is_assigned = False
                        else:
                            trip.is_assigned = True
                            
                        for driver_trip in trip.driver_trips.all():
                            if driver_trip.driver.user.id == request.auth.user.id:
                                trip.is_signed_up = True
                            else:
                                trip.is_signed_up = False
                    

                    center_point = (lat, lng)
                    test_point = (trip.origin.lat, trip.origin.lng)
                
                    distance_away = great_circle(center_point, test_point).mi
                    
                    # trip.pick_up_radius
                    
                    if distance_away < 20:
                        filtered_trips.append(trip)
                    
                    # calculate distance between center point and test point
                    # add trips that have origin within radius
                    
                    
        

                
                
                
                
                
               
            
            try:
                for passenger_trip in filtered_trips:
                    
                    point_objects = []
                    raw_points = polyline.decode(passenger_trip.path)
                
                    
                    for point in raw_points:
                        a = {
                            "lat": point[0],
                            "lng": point[1]
                        }
                        point_objects.append(a)
                    passenger_trip.path_points = point_objects
                
                
            except:
                pass

        

            serializer = PassengerTripSerializer(filtered_trips, many = True)
            return Response(serializer.data, status=status.HTTP_200_OK)

            
        except:
            serializer = PassengerTripSerializer(passenger_trips, many = True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
    
    
    def retrieve(self, request, pk):
        
        passenger_trip = PassengerTrip.objects.get(pk = pk)
        
        if passenger_trip.Passenger.user == request.auth.user:
            passenger_trip.is_user = True
        else:
            passenger_trip.is_user = False
        
       
        
        point_objects = []
        raw_points = polyline.decode(Passenger_trip.path)
    
        
        for point in raw_points:
            a = {
                "lat": point[0],
                "lng": point[1]
            }
            point_objects.append(a)
        passenger_trip.path_points = point_objects
        
        serializer = PassengerTripSerializer(passenger_trip)
        
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    
    def create(self, request):
        
        # first create location entries for the destination and origin
        # set the key as the latitude
        
        passenger = Member.objects.get(user = request.auth.user)
        
        
        
        origin = Location.objects.create(
            lat = request.data['origin']['lat'],
            lng = request.data["origin"]['lng'],
      
            
        )
        
        destination = Location.objects.create(
            lat = request.data['destination']['lat'],
            lng = request.data["destination"]['lng'],
  
      
        )
        
        request.data['creation_date'] = datetime.datetime.now()
        request.data['passenger'] = passenger.id
        request.data["origin"] = origin.id
        request.data['destination'] = destination.id
        serializer = CreatePassengerTripSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    def update(self, request, pk):
        """update existing PassengerTrip"""
        
        passenger_trip = PassengerTrip.objects.get(pk = pk)
        
        serializer = UpdatePassengerTripSerializer(passenger_trip, data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    
        
        return Response(None, status=status.HTTP_200_OK)
        
    def destroy(self, request, pk):
        passenger_trip = PassengerTrip.objects.get(pk = pk)
        
        passenger_trip.delete()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    
    
    @action(methods=['put'], detail=True)
    def sign_up_passenger(self, request, pk):
        
        passenger_trip = PassengerTrip.objects.get(pk = pk)
        
        origin = Location.objects.get(pk = request.data['origin']['id'])
        destination = Location.objects.get(pk = request.data['destination']['id'])
        
        passenger = Member.objects.get(user = request.auth.user)
        
        passenger_trip = PassengerTrip.objects.create(
            passenger = passenger,
            origin = origin,
            destination = destination,
            creation_date = datetime.datetime.now(),
            start_date = request.data['start_date'],
            trip_distance = request.data['trip_distance'],
            expected_travel_time = request.data['expected_travel_time'],
            trip_summary = request.data['trip_summary'],
            path = request.data['path']
            
            
        )
        
        
        passenger_trip.passenger_trips.add(passenger_trip.id)
        
        
        return Response("Passenger added", status=status.HTTP_200_OK)
        
        
    @action(methods=['put'], detail=True)
    def remove_passenger(self, request, pk):
        
        
        passenger_trip = PassengerTrip.objects.get(pk = pk)
        
        passenger_trip = Passenger_trip.passenger_trips.get(passenger__user = request.auth.user)



        
        
        
        
        
        Passenger_trip.passenger_trips.remove(passenger_trip.id)
        
        passenger_trip.delete()
        
        
        return Response("Passenger added", status=status.HTTP_200_OK)
        
    
    