import uuid
# Django imports
from django.db.models import JSONField
from django.contrib.gis.db import models

# Create your models here.


class RideRequest(models.Model):
    """
    Basic Model to store ride request details
    """

    ride_id = models.CharField(max_length=100, blank=False, unique=True, default=uuid.uuid4)
    passenger_id = models.IntegerField()
    pickup_location = models.PointField(geography=True)
    drop_location = models.PointField(geography=True)
    preferences = JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    