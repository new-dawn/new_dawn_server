from django.contrib.auth.models import User
from django.db import models

from new_dawn_server.users.models import Profile


class Image(models.Model):
    caption = models.CharField(blank=True, max_length=200, null=True)
    media = models.ImageField(upload_to='images/')
    order = models.IntegerField(blank=True, null=True)
    profile = models.ForeignKey(Profile, blank=True, on_delete=models.SET_NULL, null=True)
    update_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
    	ordering = ['order']