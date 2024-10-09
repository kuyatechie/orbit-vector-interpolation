from .models import OrbitVector
from django.http import Http404
from datetime import timedelta, datetime
from enum import Enum

class Precision(Enum):
    YEAR = "1 year"
    MONTH = "1 month"
    DAY = "1 day"
    HOUR = "1 hour"
    MINUTE = "1 minute"
    SECOND = "1 second"
    MILLISECOND = "1 millisecond"

class Interpolator():
    def __init__(self, interpolate_time):
        self.interpolate_time = datetime.fromisoformat(interpolate_time)

    def get_previous_entry(self):
        if OrbitVector.objects.filter(time__lte=self.interpolate_time).exists():
            return OrbitVector.objects.filter(time__lte=self.interpolate_time).order_by('time').last()
        else:
            raise Http404
    
    def get_next_entry(self):
        if OrbitVector.objects.filter(time__gte=self.interpolate_time).exists():
            return OrbitVector.objects.filter(time__gte=self.interpolate_time).order_by('time').first()
        else:
            raise Http404

    def generate_time_bucket(self, prev_time, next_time, interval):
        return OrbitVector.objects.raw(
            """SELECT
                1 as id,
                '{}' as time,
                time_bucket_gapfill(
                    '{}', time,
                    start => '{}', 
                    finish => '{}') as interval,
                interpolate(avg(posx)) as posx,
                interpolate(avg(posy)) as posy,
                interpolate(avg(posz)) as posz,
                interpolate(avg(velx)) as velx,
                interpolate(avg(vely)) as vely,
                interpolate(avg(velz)) as velz
            FROM data_orbitvector
            WHERE time between '{}' and '{}'
            GROUP BY interval
            ORDER BY interval""".format(self.interpolate_time, interval, prev_time, next_time, prev_time, next_time)
        )

    def interpolate_vector(self, prev_time, next_time, interval):
        time_bucket = self.generate_time_bucket(prev_time, next_time, interval)
        for vector in time_bucket:
            if getattr(vector, "interval") > self.interpolate_time:
                return vector
        return None

    def get_interval(self, prev_time, next_time):
        delta = next_time-prev_time
        if delta <= timedelta(seconds=30):
            return Precision.MILLISECOND
        if delta <= timedelta(minutes=30):
            return Precision.SECOND
        elif delta <= timedelta(hours=12):
            return Precision.MINUTE
        elif delta <= timedelta(days=15):
            return Precision.HOUR
        elif delta <= timedelta(days=180):
            return Precision.DAY
        elif delta <= timedelta(days=18250):
            return Precision.MONTH
        else:
            return Precision.YEAR

    def generate(self):
        prev_time = getattr(self.get_previous_entry(), "time")
        next_time = getattr(self.get_next_entry(), "time")

        if prev_time == None or next_time == None:
            return None

        if prev_time == next_time:
            return OrbitVector.objects.get(time=self.interpolate_time)
        
        precision = self.get_interval(prev_time, next_time)
        return self.interpolate_vector(prev_time, next_time, precision.value)
