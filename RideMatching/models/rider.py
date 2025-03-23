import uuid
# Django imports
from django.contrib.gis.db import models
from django.db.models import JSONField

class Driver(models.Model):
    """
    Model to store driver details
    """


    DriverStatus = (
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('unavailable', 'Unavailable')
    )

    driver_id = models.CharField(max_length=100, blank=False, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    location = models.PointField(geography=True)  # Stores (latitude, longitude)
    rating = models.FloatField(default=5.0)
    preferences = JSONField(default=dict) # Stores preferences of the driver
    status = models.CharField(
        max_length=15,
        choices=DriverStatus,
        default="available"
    )


