from django.db import models

from datetime import datetime


class Block(models.Model):
    user_account_block = models.ForeignKey("users.Account", on_delete=models.CASCADE, related_name="toblock")
    user_account_blocked = models.ForeignKey("users.Account", on_delete=models.SET_NULL, related_name="fromblock",
                                             null=True)
    update_time = models.DateField(auto_now_add=True)


class Grade(models.Model):
    user_account_given = models.ForeignKey("users.Account", on_delete=models.CASCADE, related_name="tograde")
    user_account_received = models.ForeignKey("users.Account", on_delete=models.SET_NULL, related_name="fromgrade",
                                              null=True)
    grade = models.IntegerField(blank=True)
    update_time = models.DateField(default=datetime.now)


class Like(models.Model):
    user_profile_like = models.ForeignKey("users.Profile", on_delete=models.CASCADE, related_name="tolike")
    user_profile_liked = models.ForeignKey("users.Profile", on_delete=models.SET_NULL, related_name="fromlike",
                                           null=True)
    match = models.BooleanField(blank=True)
    like_time = models.DateField(auto_now_add=True)


class Relationship(models.Model):
    user_account_relationship_invite = models.ForeignKey("users.Account", on_delete=models.CASCADE,
                                                         related_name="torelation")
    user_account_relationship_receive = models.ForeignKey("users.Account", on_delete=models.CASCADE,
                                                          related_name="fromrelation")
    in_relationship = models.IntegerField(blank=True)
    update_time = models.DateField(default=datetime.now)
