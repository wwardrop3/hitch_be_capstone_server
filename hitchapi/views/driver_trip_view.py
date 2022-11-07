from ast import Pass
from crypt import methods
import datetime
from lib2to3.pgen2 import driver
from os import stat
from re import M
from sqlite3 import Date
from typing import final
from xmlrpc.client import DateTime
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from hitchapi.models.DriverTripRating import DriverTripRating
from hitchapi.models.Location import Location
from rest_framework.decorators import action
import polyline
from geopy import distance
from geopy.distance import great_circle, geodesic
from django.db.models import Q



from hitchapi.models.DriverTrip import DriverTrip
from hitchapi.models.Member import Member
from hitchapi.models.Message import Message
from hitchapi.models.PassengerTrip import PassengerTrip
from hitchapi.serializers.driver_trip_serializer import CreateDriverTripSerializer, DriverTripSerializer, UpdateDriverTripSerializer
from hitchapi.serializers.passenger_trip_serializer import PassengerTripSerializer 

class DriverTripView(ViewSet):
    
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
                    
                    if trip.completed == True or trip.start_date < datetime.date.today():
                        pass
                    
                    
                    else:
                    
                        
                        
                        if trip.driver.user == request.auth.user:
                            trip.is_user = True
                        else:
                            trip.is_user = False
                            
                            if len(trip.passenger_trips.all()) == 0:
                                trip.is_assigned = False
                            else:
                                trip.is_assigned = True
                                
                            for passenger_trip in trip.passenger_trips.all():
                                if passenger_trip.passenger.user.id == request.auth.user.id:
                                    trip.is_signed_up = True
                                else:
                                    trip.is_signed_up = False
                        

                        center_point = (lat, lng)
                        test_point = (trip.origin.lat, trip.origin.lng)
                    
                        distance_away = great_circle(center_point, test_point).mi
                        
                        # trip.pick_up_radius
                        
                        if distance_away < trip.detour_radius:
                            filtered_trips.append(trip)
                        
                        # calculate distance between center point and test point
                        # add trips that have origin within radius
                        
                        
            

                
                
                
                
                
               
            
            try:
                for driver_trip in filtered_trips:
                    
                    point_objects = []
                    raw_points = polyline.decode(driver_trip.path)
                
                    
                    for point in raw_points:
                        a = {
                            "lat": point[0],
                            "lng": point[1]
                        }
                        point_objects.append(a)
                    driver_trip.path_points = point_objects
                
                
            except:
                pass

        

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
    
        
        for point in raw_points:
            a = {
                "lat": point[0],
                "lng": point[1]
            }
            point_objects.append(a)
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
        

        
        serializer = UpdateDriverTripSerializer(driver_trip, data = request.data)
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
        
        sender = Member.objects.get(user = request.auth.user)
        
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
            path = request.data['path'],
            is_approved = False
            
            
        )
        
        new_message = Message.objects.create(
            driver_trip = driver_trip,
            passenger_trip=passenger_trip,
            creation_date = datetime.datetime.now(),
            is_read = False,
            message_text = "Passenger Trip Requested",
            sender = sender,
            receiver=driver_trip.driver
            
        )
        
        
        driver_trip.passenger_trips.add(passenger_trip.id)
        
        
        return Response("Trip added", status=status.HTTP_200_OK)
        
        
    @action(methods=['put'], detail=True)
    def remove_passenger(self, request, pk):
        
        
        driver_trip = DriverTrip.objects.get(pk = pk)
        
        passenger_trip = driver_trip.passenger_trips.get(passenger__user = request.auth.user)

        message = Message.objects.filter(passenger_trip = passenger_trip, driver_trip=driver_trip)
        
        message.delete()


        
        
        
        
        
        driver_trip.passenger_trips.remove(passenger_trip.id)
        
        passenger_trip.delete()
        
        
        return Response("Trip Deleted", status=status.HTTP_200_OK)


    @action(methods=['post'], detail=False)
    def get_driver_trips_by_passenger_trip(self, request):
        
        trip_origin = (request.data['origin']['lat'], request.data['origin']['lng'])
        trip_destination = (request.data['destination']['lat'], request.data['destination']['lng'])
        
        passenger_trip_distance = geodesic(trip_origin, trip_destination).mi
        
        # first filter driver trips by those that start after the passenger_trip start date
        driver_trips = DriverTrip.objects.filter(start_date__gt = request.data['start_date'])
        
        detailed_trips = []  
         
        # assigning detail of ALL driver trips that occur after passenger trip starting date
        for trip in driver_trips:
            
            if trip.completed == True:
                pass
            
            else:
            
                
                
                if trip.driver.user == request.auth.user:
                    trip.is_user = True
                    pass
              
                else:
                    trip.is_user = False
                    
                    if len(trip.passenger_trips.all()) == 0:
                        trip.is_assigned = False
                        
                    else:
                        trip.is_assigned = True
                        
                        
                    for passenger_trip in trip.passenger_trips.all():
                        if passenger_trip.passenger.user.id == request.auth.user.id:
                            trip.is_signed_up = True
                        else:
                            trip.is_signed_up = False
                            pass
                
                    point_objects = []
                    raw_points = polyline.decode(trip.path)
                
                    
                    for index, point in enumerate(trip.path):
                        if index % 3 == 0:
                            a = {
                                "lat": point[0],
                                "lng": point[1]
                            }
                            point_objects.append(a)
                    trip.path = point_objects
                    

                    detailed_trips.append(trip)
                    
        
    

        
        
        
        
        
        nearby_trips = []
        far_trips = []
        shortest_distance = 100000000
        best_trips = []
        

        # for each detailed trip that is close by to passenger trip, pop it out and append to nearby trips
        for trip in detailed_trips:
       
            
            
            center_point = (request.data['origin']['lat'], request.data['origin']['lng'])
            test_point = (trip.origin.lat, trip.origin.lng)
        
            distance_away = great_circle(center_point, test_point).mi
            
            # it its close by to start, add to nearby trips list
            if distance_away < trip.detour_radius:
                
    
                nearby_trips.append(trip)
                
                
            else:
                far_trips.append(trip)
               
                
        
            
                
            
 

        
        final_trips = set()
        
        far_trip_point_break = False
        nearby_trip_point_break = False
        far_trip_break = False
        
        # for each nearby trip
        for nearby_trip in nearby_trips:
            
            nearby_trip_destination = (nearby_trip.destination.lat, nearby_trip.destination.lng)
            nearby_trip_distance = geodesic(nearby_trip_destination, trip_destination).mi

            
            

            
           

            # for each far trip
            for far_trip in far_trips:
                far_trip_destination = (far_trip.destination.lat, far_trip.destination.lng)    
                far_trip_distance = geodesic(far_trip_destination, trip_destination).mi
                
                
                
                
                # if the far trip doesnt get the person closer to their destination, no need to search the points **can do this with 1 connection would not with 2 connections
                if far_trip_distance > passenger_trip_distance:
                    pass
    


             
                for nearby_trip_point in nearby_trip.path:
                    
               
    
                    for far_trip_point in far_trip.path:
                    
                        
                        
                
                        center_point = (nearby_trip_point['lat'], nearby_trip_point['lng'])
                        test_point = (far_trip_point['lat'], far_trip_point['lng'])
                    
                        distance_away = great_circle(center_point, test_point).mi
                        
                        
                            
                        if distance_away < nearby_trip.detour_radius:
                            
                            
                        #    if there is an intersection and the far trip destination is closer than passenger now
                            if far_trip_distance < passenger_trip_distance:
                                
                                if far_trip_distance < shortest_distance:
                                    shortest_distance = far_trip_distance
                                    best_trips = [nearby_trip, far_trip]
                                    
                                final_trips.add(nearby_trip)
                                final_trips.add(far_trip)
                                nearby_trip_point_break = True
                                break
                            
                            # if there is an intersection but the far trip isnt closer, check to see if the nearby trip gets closer or not
                            elif nearby_trip_distance < passenger_trip_distance:
                                
                                if nearby_trip_distance < shortest_distance:
                                    shortest_distance = nearby_trip_distance
                                    best_trips=[nearby_trip]
                                    
                                final_trips.add(nearby_trip)
                                nearby_trip_point_break = True
                                break
                            
                        #     # if there is no intersection but the nearby trip still gets you closer, add it
                        elif nearby_trip_distance < passenger_trip_distance:
                            if nearby_trip_distance < shortest_distance:
                                    shortest_distance = nearby_trip_distance
                                    best_trips=[nearby_trip]
                                    
                            final_trips.add(nearby_trip)
                            nearby_trip_point_break = True
                            pass
                            

                                
                    if nearby_trip_point_break ==True:
                        far_trip_break = True
                        pass
                # if far_trip_break ==True:
                #     pass
               

        
        
        for final_trip in final_trips:
            for best_trip in best_trips:
                if final_trip.id == best_trip.id:
                    final_trip.is_recommended = True
                    break
                else:
                    final_trip.is_recommended = False
        
       

        
        
        
        serializer = DriverTripSerializer(final_trips, many = True)

        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    