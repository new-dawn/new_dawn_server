from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from phonenumber_field .modelfields import PhoneNumberField


# An account model
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField()
    creation_date = models.DateField(auto_now_add=True)
    # a google's library for international phone number
    phone_number = PhoneNumberField(default='000000000')
    gender = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')), default='M')


# An account's profile information
class Profile(models.Model):
    account = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        verbose_name = 'the user'
    )
    profile_photo_url = models.CharField(max_length=1000)
    description = models.CharField(max_length=200)
    #city and hometown can later be changed to location library
    city = models.CharField(max_length=50, default='new york')
    employer = models.CharField(max_length=50, default='google')
    job_title = models.CharField(max_length=50, default='analyst')
    #School can be expanded further
    school = models.CharField(max_length=50, default='nyu')
    height = models.DecimalField(max_digits=2, decimal_places=2, default='1.12')
    smoke = models.BooleanField(default=True)

