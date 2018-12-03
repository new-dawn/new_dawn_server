from new_dawn_server.questions.models import AnswerQuestion, Question
from new_dawn_server.users.api.resources import UserResource
from tastypie import fields
from tastypie.resources import ModelResource


class QuestionResource(ModelResource):
    class Meta:
        allowed_methods = ["get"]
        queryset = Question.objects.all()
        resource_name = "question"


class AnswerQuestionResource(ModelResource):
    question = fields.ForeignKey(QuestionResource, "question", related_name="answer_question", full=True)
    user = fields.ToOneField(UserResource, "user", related_name="answer_question", full=True)

    class Meta:
        allowed_methods = ["get"]
        queryset = AnswerQuestion.objects.all()
        resource_name = "answer_question"
