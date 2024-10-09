from django.contrib.gis.db import models
from timescale.db.models.fields import TimescaleDateTimeField
from timescale.db.models.managers import TimescaleManager


class TimescaleModel(models.Model):
    """
    A helper class for using Timescale within Django, has the TimescaleManager and
    TimescaleDateTimeField already present. This is an abstract class it should
    be inheritted by another class for use.
    """
    time = TimescaleDateTimeField(interval="1 day")

    objects = TimescaleManager()

    class Meta:
        abstract = True


class OrbitVector(TimescaleModel):
    posx = models.FloatField(null=False, blank=False, editable=False)
    posy = models.FloatField(null=False, blank=False, editable=False)
    posz = models.FloatField(null=False, blank=False, editable=False)
    velx = models.FloatField(null=False, blank=False, editable=False)
    vely = models.FloatField(null=False, blank=False, editable=False)
    velz = models.FloatField(null=False, blank=False, editable=False)
