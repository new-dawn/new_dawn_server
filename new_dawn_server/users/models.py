from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from new_dawn_server.pusher.notification_service import NotificationService
from new_dawn_server.users.constants import UserReviewStatus


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
    
    __current_review_status = None
    
    def __init__(self, *args, **kwargs):
        super(Profile, self).__init__(*args, **kwargs)
        self.__current_review_status = self.review_status
        
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.review_status == UserReviewStatus.NORMAL.value \
                and self.__current_review_status == UserReviewStatus.PENDING.value:
            NotificationService().send_notification([str(self.user_id)], message="Your profile is now activated!")
        super(Profile, self).save(force_insert, force_update, *args, **kwargs)
        self.__current_review_status = self.review_status

    def __str__(self):
        return self.account.name + "_profile"
