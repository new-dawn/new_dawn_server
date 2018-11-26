from django.db import models


class Questions(models.Model):
    question = models.CharField(max_length=150, blank=True)
    sample_answer = models.CharField(max_length=150, blank=True, null=True)


class AnswerQuestions(models.Model):
    answer = models.CharField(max_length=150)
    order = models.IntegerField()
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    update_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user = models.ForeignKey("users.Profile", on_delete=models.CASCADE,
                             null=True, blank=True)
