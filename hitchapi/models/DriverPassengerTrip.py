from django.db import models



class DriverPassengerTrip(models.Model):
    driver_trip = models.ForeignKey("DriverTrip", on_delete=models.CASCADE)
    passenger_trip = models.ForeignKey("PassengerTrip", on_delete=models.CASCADE)