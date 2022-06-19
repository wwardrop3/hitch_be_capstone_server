from django.db import models




class DriverTrip(models.Model):
    driver = models.ForeignKey("Member", on_delete=models.CASCADE) 
    origin = models.ForeignKey("Location", on_delete=models.CASCADE, related_name="trip_origin")
    destination = models.ForeignKey("Location", on_delete=models.CASCADE, related_name="trip_destination")
    origin_place = models.TextField()
    destination_place = models.TextField()
    creation_date = models.DateTimeField()
    start_date = models.DateTimeField()
    completion_date = models.DateTimeField(null=True)
    detour_radius = models.IntegerField()
    trip_distance = models.FloatField()
    expected_travel_time = models.FloatField()
    trip_summary = models.TextField(null=True)
    seats = models.IntegerField()
    completed = models.BooleanField()
    tags = models.ManyToManyField("Tag",through="TripTag", related_name="trips")
    passenger_trips = models.ManyToManyField("PassengerTrip", through="DriverPassengerTrip", related_name="driver_trips")
    path = models.TextField()
    
    @property
    def path_points(self):
        return self.__path_points
    @path_points.setter
    def path_points(self, value):
        self.__path_points = value


    @property
    def is_user(self):
        return self.__is_user
    @is_user.setter
    def is_user(self, value):
        self.__is_user = value
        
    @property
    def is_signed_up(self):
        return self.__is_signed_up
    @is_signed_up.setter
    def is_signed_up(self, value):
        self.__is_signed_up = value
        
        
    @property
    def is_assigned(self):
        return self.__is_assigned
    @is_assigned.setter
    def is_assigned(self, value):
        self.__is_assigned = value