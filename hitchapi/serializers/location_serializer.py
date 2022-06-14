from rest_framework.serializers import ModelSerializer

from hitchapi.models.Location import Location


class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = ("id", "lat", "lng")
        

class CreateLocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = ("lat", "lng")