from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# An account model
class Account(models.Model):
    birthday = models.DateField(blank=True, null=True)
    city_preference = models.ManyToManyField("locations.CityPreference")
    creation_date = models.DateField(auto_now_add=True)
    gender = models.CharField(blank=True, choices=(('M', 'Male'), ('F', 'Female')), max_length=1, null=True)
    name = models.CharField(blank=True, max_length=20, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# An account's profile information
class Profile(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    age = models.IntegerField(blank=True, null=True)
    # city and hometown can later be changed to location library
    degree = models.CharField(blank=True, max_length=50, null=True)
    description = models.CharField(blank=True, max_length=200, null=True)
    drink = models.CharField(blank=True, max_length=50, null=True)
    employer = models.CharField(blank=True, max_length=50, null=True)
    height = models.IntegerField(blank=True, null=True)
    hometown = models.CharField(blank=True, max_length=50, null=True)
    job_title = models.CharField(blank=True, max_length=50, null=True)
    location = models.CharField(blank=True, max_length=50, null=True)
    profile_photo_url = models.CharField(blank=True, max_length=50, null=True)
    review_status = models.IntegerField(blank=True, null=True)
    # school can be expanded further
    school = models.CharField(blank=True, max_length=50, null=True)
    smoke = models.CharField(blank=True, max_length=50, null=True)
    update_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.account.name + "_profile"
