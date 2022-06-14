from crypt import methods
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
            city = request.data['origin']['city'],
            state = request.data['origin']['state']
        )
        
        destination = Location.objects.create(
            lat = request.data['destination']['lat'],
            lng = request.data["destination"]['lng'],
            city = request.data['destination']['city'],
            state = request.data['destination']['state']
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
    
    

    @action(methods=['get'], detail=False)
    def driver_trips_by_passenger_trip(self, request):
        
        driver_trips = DriverTrip.objects.all()
        
        request.data['path_points'] = polyline.decode(request.data['path'])
        
        
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
            
            # first getting 1st set of trips in my area
            center_point = (request.data['origin']['lat'], request.data['origin']['lat'])
            test_point = (trip.origin.lat, trip.origin.lng)
        
            distance_away = great_circle(center_point, test_point).mi
            
    
            # if trip is in my area, then check other driving trips that cross the paths of the trips
            if distance_away < trip.detour_radius:
                driver_trip_break = False
                path_point_break = False
                
                filtered_trips.append(trip)
                    
        
                for driver_trip in driver_trips:
                            
                    point_objects = []
                    raw_points = polyline.decode(driver_trip.path)
                
                    
                    for point in raw_points:
                        a = {
                            "lat": point[0],
                            "lng": point[1]
                        }
                        point_objects.append(a)
                    
                    
                    for path_point in request.data.path_points:
                        
                    
                        for driver_point in path_point:
                            
                            center_point = (path_point[0], path_point[1])
                            test_point = (driver_point['lat'], driver_point['lng'])
                        
                            distance_away = great_circle(center_point, test_point).mi
                            
                        
                            if distance_away < request.data['detour_radius']:
                                print(distance_away)
                                
                                driver_trip_serializer = DriverTripSerializer(driver_trip)
                        
                        
                                filtered_trips.append(driver_trip)
                                path_point_break = True
                                break
                            
                        if path_point_break:
                            driver_trip_break = True
                            break
                    
                    if driver_trip_break:
                        break
                    
        print(filtered_trips)
        serializer = PassengerTripSerializer(passenger_trip)
                                
            
        
                            
            
            
            
            
            
                
    
            
        
        
                