from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# An account model
class Account(models.Model):
    birthday = models.DateField()
    creation_date = models.DateField(auto_now_add=True)
    gender = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')), blank=True)
    phone_number = PhoneNumberField(blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


# An account's profile information
class Profile(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    # city and hometown can later be changed to location library
    city_preference = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=200)
    employer = models.CharField(max_length=50, blank=True)
    height = models.DecimalField(max_digits=2, decimal_places=2, blank=True, null=True)
    hometown = models.CharField(max_length=50, blank=True)
    job_title = models.CharField(max_length=50, blank=True)
    profile_photo_url = models.CharField(max_length=1000)
    # school can be expanded further
    school = models.CharField(max_length=50, blank=True)
    smoke = models.BooleanField(blank=True, null=True)