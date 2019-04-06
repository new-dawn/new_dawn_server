from django.contrib.auth.models import User
from django.db import models
from new_dawn_server.users.models import Profile


class Question(models.Model):
    question = models.CharField(max_length=150)
    sample_answer = models.CharField(blank=True, max_length=150, null=True)
    user_defined = models.BooleanField(blank=True, null=True)


class AnswerQuestion(models.Model):
    answer = models.CharField(max_length=150)
    order = models.IntegerField(blank=True, null=True)
    profile = models.ForeignKey(Profile, blank=True, on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    update_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
