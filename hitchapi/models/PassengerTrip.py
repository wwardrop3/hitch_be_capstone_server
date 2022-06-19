

from django.db import models



class PassengerTrip(models.Model):
    passenger = models.ForeignKey("Member", on_delete=models.CASCADE)
    origin = models.ForeignKey("Location", on_delete=models.CASCADE, related_name="passenger_trip_origin")
    destination = models.ForeignKey("Location", on_delete=models.CASCADE, related_name="passenger_trip_destination")
    origin_place = models.TextField()
    destination_place=models.TextField()
    creation_date = models.DateTimeField()
    start_date = models.DateTimeField()
    completion_date = models.DateTimeField(null=True)
    trip_distance = models.FloatField()
    expected_travel_time = models.FloatField()
    trip_summary = models.TextField(null=True)
    path = models.TextField()
    is_approved = models.BooleanField()
    
    @property
    def path_points(self):
        return self.__path_points
    @path_points.setter
    def path_points(self, value):
        self.__path_points = value
        
    @property
    def recommended_trips(self):
        return self.__recommended_trips
    @recommended_trips.setter
    def recommended_trips(self, value):
        self.__recommended_trips = value


