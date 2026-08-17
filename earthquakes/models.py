from django.db import models

class Earthquake(models.Model):
    external_id = models.CharField(max_length=50, unique=True)
    magnitude = models.FloatField()
    place = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    depth = models.FloatField()
    time = models.DateTimeField()
    sig = models.IntegerField()
    fetched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.place} {self.magnitude}'
