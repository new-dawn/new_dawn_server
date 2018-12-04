from new_dawn_server.questions.models import AnswerQuestion, Question
from new_dawn_server.users.api.resources import UserResource
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS

ANSWER_QUESTION_FIELDS = {
    "answer": True,
    "order": True,
}

QUESTION_FIELDS = {
    "question": True,
    "sample_answer": True,
}


class QuestionResource(ModelResource):
    class Meta:
        always_return_data = True
        authorization = Authorization()
        allowed_methods = ["get", "post"]
        queryset = Question.objects.all()
        resource_name = "question"


class AnswerQuestionResource(ModelResource):
    question = fields.ForeignKey(QuestionResource, "question", related_name="answerquestion", full=True)
    user = fields.ForeignKey(UserResource, "user", related_name="answerquestion", full=True)

    class Meta:
        always_return_data = True
        authorization = Authorization()
        allowed_methods = ["get", "post"]
        queryset = AnswerQuestion.objects.all()
        resource_name = "answerquestion"
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'question': ALL_WITH_RELATIONS,
        }
