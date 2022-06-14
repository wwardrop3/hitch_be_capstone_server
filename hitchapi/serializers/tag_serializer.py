from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User

from hitchapi.models.Tag import Tag

class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")
        

class CreateTagSerializer(ModelSerializer):
    # only admins can create tags
    class Meta:
        model = Tag
        fields=("name",)