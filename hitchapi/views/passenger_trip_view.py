import datetime
from lib2to3.pgen2 import driver
from os import stat
from re import M
from sqlite3 import Date
from xmlrpc.client import DateTime
import polyline
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from hitchapi.models.DriverTrip import DriverTrip
from hitchapi.models.Location import Location
from hitchapi.models.Member import Member
from rest_framework.decorators import action

import polyline
from geopy import distance
from geopy.distance import great_circle


from hitchapi.models.PassengerTrip import PassengerTrip
from hitchapi.serializers.driver_trip_serializer import DriverTripSerializer
from hitchapi.serializers.passenger_trip_serializer import CreatePassengerTripSerializer, PassengerTripSerializer 

class PassengerTripView(ViewSet):
    
    def list(self, request):
        """get all PassengerTrips from a user"""
        passenger_trips = PassengerTrip.objects.all()
        
        serializer = PassengerTripSerializer(passenger_trips, many = True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    
    
    def retrieve(self, request, pk):
        passenger_trip = PassengerTrip.objects.get(pk = pk)
        
        passenger_trip.path_points = polyline.decode(passenger_trip.path)
        
        driver_trips = DriverTrip.objects.all()
        
        
        recommended_trips =[]
        
        driver_trip_break = False
        path_point_break = False
        
        for driver_trip in driver_trips:
                    
                point_objects = []
                raw_points = polyline.decode(driver_trip.path)
            
                
                for point in raw_points:
                    a = {
                        "lat": point[0],
                        "lng": point[1]
                    }
                    point_objects.append(a)
                
                
                for path_point in passenger_trip.path_points:
                    
                
                    for driver_point in point_objects:
                        
                        center_point = (path_point[0], path_point[1])
                        test_point = (driver_point['lat'], driver_point['lng'])
                    
                        distance_away = great_circle(center_point, test_point).mi
                        
                     
                        if distance_away < 20:
                            print(distance_away)
                            
                            driver_trip_serializer = DriverTripSerializer(driver_trip)
                    
                    
                            recommended_trips.append(driver_trip_serializer.data)
                            path_point_break = True
                            break
                        
                    if path_point_break:
                        driver_trip_break = True
                        break
                
                if driver_trip_break:
                    break
                        
                        
        
        
        
        
        passenger_trip.recommended_trips = recommended_trips
        serializer = PassengerTripSerializer(passenger_trip)
        
        
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def create(self, request):
    
        passenger = Member.objects.get(user = request.auth.user)
        
        
        
        origin = Location.objects.create(
            lat = request.data['origin']['lat'],
            lng = request.data["origin"]['lng'],
  
        )
        
        destination = Location.objects.create(
            lat = request.data['destination']['lat'],
            lng = request.data["destination"]['lng'],
       
        )
        
        request.data['passenger'] = passenger.id
        request.data["origin"] = origin.id
        request.data['destination'] = destination.id
        serializer = CreatePassengerTripSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

        
    def destroy(self, request, pk):
        passenger_trip = PassengerTrip.objects.get(pk = pk)
        
        passenger_trip.delete()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    
    def update(self, request, pk):
        
        passenger_trip = PassengerTrip.objects.get(pk = pk)
        
        request.data['origin'] = request.data['origin']['id']
        request.data['destination'] = request.data['destination']['id']
        

        
        serializer = CreatePassengerTripSerializer(passenger_trip, data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(None, status=status.HTTP_200_OK)
    
    
    @action(methods=['get'], detail=True)
    def trip_decode(self, request, pk):
        
        
        
        passenger_trip = PassengerTrip.objects.get(pk = pk)
        
        passenger_trip.path_points = polyline.decode(passenger_trip.path)
        
        serializer = PassengerTripSerializer(passenger_trip)
        
        return Response(serializer.data)
    
    
    @action(methods=['get'], detail=False)
    def trips_decode(self, request):
        
        passenger_trips = PassengerTrip.objects.all()
        
        for passenger_trip in passenger_trips:
            point_objects = []
            rawPoints = polyline.decode(passenger_trip.path)
            for point in rawPoints[0:7]:
                    a = {
                        "lat": point[0],
                        "lng": point[1]
                    }
                    point_objects.append(a)
            passenger_trip.path_points = point_objects
        
        serializer = PassengerTripSerializer(passenger_trips, many = True)
        
        return Response(serializer.data)
    
    