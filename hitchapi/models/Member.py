from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
    bio = models.CharField(max_length=201)
    profile_image_url = models.CharField(max_length=201)
    created_on = models.DateTimeField()
    active = models.BooleanField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    @property
    def passenger_trips(self):
        return self.__passenger_trips
    @passenger_trips.setter
    def passenger_trips(self, value):
        self.__passenger_trips = value
        
    @property
    def driver_trips(self):
        return self.__driver_trips
    @driver_trips.setter
    def driver_trips(self, value):
        self.__driver_trips = value
