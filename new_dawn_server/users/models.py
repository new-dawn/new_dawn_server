from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# An account model
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField()
    creation_date = models.DateField(auto_now_add=True)

# An account's profile information
class Profile(models.Model):
    account = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        verbose_name = 'the user'
    )
    profile_photo_url = models.CharField(max_length=1000)
    description = models.CharField(max_length=200)
