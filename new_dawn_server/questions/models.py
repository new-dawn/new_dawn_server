from django.db import models


class Questions(models.Model):
    user_profile = models.ForeignKey("users.Profile", on_delete=models.CASCADE, related_name="from_user",
                                     null=True, blank=True)
    user_question = models.CharField(max_length=150, blank=True)
    sample_answer = models.CharField(max_length=150, blank=True, null=True)


class Answers(models.Model):
    question = models.OneToOneField(Questions, on_delete=models.CASCADE)
    answer = models.CharField(max_length=150, blank=True)
