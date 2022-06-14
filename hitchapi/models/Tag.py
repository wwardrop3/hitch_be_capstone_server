from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.TextField()
    
