from django.db import models


class Answers(models.Model):
    answer = models.CharField(max_length=150, blank=True)


class Questions(models.Model):
    question = models.CharField(max_length=150, blank=True)
    sample_answer = models.CharField(max_length=150, blank=True, null=True)


class AnswerQuestions(models.Model):
    answer = models.ForeignKey(Answers, on_delete=models.CASCADE, blank=True)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, blank=True)
    update_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class UsersAnswerQuestions(models.Model):
    answer_question = models.ForeignKey(AnswerQuestions, on_delete=models.CASCADE)
    question_order = models.IntegerField()
    user_profile = models.ForeignKey("users.Profile", on_delete=models.CASCADE,
                                     null=True, blank=True)
