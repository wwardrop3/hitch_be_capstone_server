from ast import Pass
from crypt import methods
import datetime
from lib2to3.pgen2 import driver
from os import stat
from re import M
from sqlite3 import Date
from xmlrpc.client import DateTime
from pytz import utc
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from hitchapi.models.Location import Location
from rest_framework.decorators import action
import polyline
from geopy import distance
from geopy.distance import great_circle


from hitchapi.models.DriverTrip import DriverTrip
from hitchapi.models.Member import Member
from hitchapi.models.PassengerTrip import PassengerTrip
from hitchapi.serializers.driver_trip_serializer import CreateDriverTripSerializer, DriverTripSerializer
from hitchapi.serializers.passenger_trip_serializer import PassengerTripSerializer 

class DriverTripView(ViewSet):
    
    
    # for
    
    def list(self, request):
        """get all trips from a user"""
        driver_trips = DriverTrip.objects.all()
        
        try:
            
            
            lat = request.query_params.get('lat', None)
            lng = request.query_params.get('lng', None)
            
            
                
            
            
            
            if lat is not None and lng is not None:
                # game_type will be the id of the gametype being queried 
                
            
                filtered_trips = []
                
                for trip in driver_trips:
                    
                    
                    if trip.driver.user == request.auth.user:
                        trip.is_user = True
                    else:
                        trip.is_user = False
                        
                        for passenger_trip in trip.passenger_trips.all():
                            if passenger_trip.passenger.user.id == request.auth.user.id:
                                trip.is_signed_up = True
                            else:
                                trip.is_signed_up = False
                    

                    center_point = (lat, lng)
                    test_point = (trip.origin.lat, trip.origin.lng)
                
                    distance_away = great_circle(center_point, test_point).mi
                    
         
                    
                    if distance_away < trip.detour_radius:
                        filtered_trips.append(trip)
                        
                    
           

                
         
                
                
                
               
            
            try:
                for driver_trip in filtered_trips:
                    
                    point_objects = []
                    raw_points = polyline.decode(driver_trip.path)
                    
                    
                    point_time_change = driver_trip.expected_travel_time / len(raw_points)
                    base_time = driver_trip.start_date
        
                    for point in raw_points:
            
                        a = {
                            "time_stamp": base_time,
                            "lat": point[0],
                            "lng": point[1]
                        }
                
                        point_objects.append(a)
                        base_time = base_time + datetime.timedelta(0,point_time_change)
                    
                    
                    
                  
                    
                    
                
                
            except:
                pass

        
            driver_trip.path_points = point_objects
            serializer = DriverTripSerializer(filtered_trips, many = True)
            return Response(serializer.data, status=status.HTTP_200_OK)

            
        except:
            serializer = DriverTripSerializer(driver_trips, many = True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
    
    
    def retrieve(self, request, pk):
        
        driver_trip = DriverTrip.objects.get(pk = pk)
        
    
        if driver_trip.driver.user == request.auth.user:
            driver_trip.is_user = True
        else:
            driver_trip.is_user = False
        
        point_objects = []
        raw_points = polyline.decode(driver_trip.path)
        
        point_time_change = driver_trip.expected_travel_time / len(raw_points)
        base_time = driver_trip.start_date
        
        for point in raw_points:
            
            a = {
                "time_stamp": base_time,
                "lat": point[0],
                "lng": point[1]
            }
            
            point_objects.append(a)
            base_time = base_time + datetime.timedelta(0,point_time_change)
            
        driver_trip.path_points = point_objects
        
        serializer = DriverTripSerializer(driver_trip)
        
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    
    def create(self, request):
        
        # first create location entries for the destination and origin
        # set the key as the latitude
        
        driver = Member.objects.get(user = request.auth.user)
        
        
        
        origin = Location.objects.create(
            lat = request.data['origin']['lat'],
            lng = request.data["origin"]['lng'],
      
            
        )
        
        destination = Location.objects.create(
            lat = request.data['destination']['lat'],
            lng = request.data["destination"]['lng'],
  
      
        )
        
        request.data['creation_date'] = datetime.datetime.now()
        request.data['driver'] = driver.id
        request.data["origin"] = origin.id
        request.data['destination'] = destination.id
        serializer = CreateDriverTripSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        driver_trip = DriverTrip.objects.get(pk = serializer.data['id'])
        driver_trip.tags.add(*request.data['tags'])
        serializer = DriverTripSerializer(driver_trip)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    def update(self, request, pk):
        """update existing DriverTrip"""
        
        driver_trip = DriverTrip.objects.get(pk = pk)
        
        serializer = CreateDriverTripSerializer(driver_trip, data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        driver_trip.tags.remove(*driver_trip.tags.all())
        driver_trip.tags.add(*request.data['tags'])
    
        
        return Response(None, status=status.HTTP_200_OK)
        
    def destroy(self, request, pk):
        driver_trip = DriverTrip.objects.get(pk = pk)
        
        driver_trip.delete()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    
    
    @action(methods=['put'], detail=True)
    def sign_up_passenger(self, request, pk):
        
        driver_trip = DriverTrip.objects.get(pk = pk)
        
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
        
        
        driver_trip.passenger_trips.add(passenger_trip.id)
        
        
        return Response("driver added", status=status.HTTP_200_OK)
        
        
    @action(methods=['put'], detail=True)
    def remove_passenger(self, request, pk):
        
        
        driver_trip = DriverTrip.objects.get(pk = pk)
        
        passenger_trip = driver_trip.passenger_trips.get(passenger__user = request.auth.user)



        
        
        
        
        
        driver_trip.passenger_trips.remove(passenger_trip.id)
        
        passenger_trip.delete()
        
        
        return Response("driver added", status=status.HTTP_200_OK)
        
    
    