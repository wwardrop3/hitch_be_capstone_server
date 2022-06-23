from django.db import models



class Message(models.Model):
    driver_trip = models.ForeignKey("DriverTrip", on_delete=models.CASCADE)
    passenger_trip = models.ForeignKey("PassengerTrip", on_delete=models.CASCADE)
    sender = models.ForeignKey("Member", on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey("Member", on_delete=models.CASCADE, related_name="receiver")
    creation_date = models.DateTimeField()
    is_read = models.BooleanField()
    message_text = models.TextField()
    