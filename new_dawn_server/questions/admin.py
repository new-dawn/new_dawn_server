from django.contrib import admin
from new_dawn_server.questions.models import AnswerQuestion
from new_dawn_server.questions.models import Question

admin.site.register(AnswerQuestion)
admin.site.register(Question)
