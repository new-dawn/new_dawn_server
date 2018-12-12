from django.db import models


class CityPreference(models.Model):
    city = models.CharField(blank=True, max_length=50, null=True)
    country = models.CharField(blank=True, max_length=50, null=True)
    state = models.CharField(blank=True, max_length=50, null=True)
