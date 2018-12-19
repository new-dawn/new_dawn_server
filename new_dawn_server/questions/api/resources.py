from new_dawn_server.questions.models import AnswerQuestion, Question
from new_dawn_server.users.api.resources import UserResource
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS

ANSWER_QUESTION_FIELDS = {
    "answer": True,
    "order": False,
}

QUESTION_FIELDS = {
    "question": True,
    "sample_answer": False,
}


class QuestionResource(ModelResource):
    class Meta:
        always_return_data = True
        authorization = Authorization()
        allowed_methods = ["get", "post"]
        filtering = {
            "user_defined": "exact"
        }
        queryset = Question.objects.all()
        resource_name = "question"


class AnswerQuestionResource(ModelResource):
    question = fields.ForeignKey(QuestionResource, "question", related_name="answer_question", full=True)
    user = fields.ForeignKey(UserResource, "user", related_name="answer_question", full=True)

    class Meta:
        always_return_data = True
        authorization = Authorization()
        allowed_methods = ["get", "post"]
        queryset = AnswerQuestion.objects.all()
        resource_name = "answer_question"
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'question': ALL_WITH_RELATIONS,
        }
