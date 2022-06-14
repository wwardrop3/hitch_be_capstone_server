from django.db import models



class TripTag(models.Model):
    driver_trip = models.ForeignKey("DriverTrip", on_delete=models.CASCADE)
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE)