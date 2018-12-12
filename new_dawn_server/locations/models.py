from django.db import models


class Country(models.Model):
    country = models.CharField(max_length=50)


class State(models.Model):
    state = models.CharField(max_length=50)
    country = models.ForeignKey('Country', on_delete=models.CASCADE)


class CityPreference(models.Model):
    city = models.CharField(max_length=50)
    state = models.ForeignKey('State', on_delete=models.CASCADE)
    user_account = models.ForeignKey('users.Account', on_delete=models.CASCADE)
