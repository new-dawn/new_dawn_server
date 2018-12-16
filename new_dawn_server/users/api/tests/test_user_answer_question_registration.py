import json

from django.contrib.auth.models import User
from django.test import TestCase
from new_dawn_server.questions.models import AnswerQuestion, Question
from new_dawn_server.users.models import Profile
from tastypie.test import ResourceTestCaseMixin


class AnswerQuestionInRegisterTest(ResourceTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.register_arguments = {
            "first_name": "test",
            "last_name": "user",
            "username": "test-user",
            "password": "test-pwd",
        }
        self.account_arguments = {
            "birthday": "1990-01-01",
            "phone_number": "+12345678900",
            "gender": "M",
        }
        self.profile_arguments = {
            "description": "nice",
            "employer": "MANMAN",
            "hometown": "NY",
            "job_title": "CEO",
            "profile_photo_url": "www",
            "school": "NYU",
            "smoke": True,
        }
        self.answer_question_arguments = {"answer_question":
            [
                {
                    "question": "how are you",
                    "order": 1,
                    "answer": "good",
                },
                {
                    "question": "How do you do",
                    "order": 2,
                    "answer": "do do"
                }
            ]
        }

    def test_register_with_answer_question(self):
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Question.objects.count(), 0)
        self.assertEqual(Profile.objects.count(), 0)
        self.assertEqual(AnswerQuestion.objects.count(), 0)

        all_arguments = {
            **self.register_arguments,
            **self.account_arguments,
            **self.profile_arguments,
            **self.answer_question_arguments
        }
        res = self.api_client.post(
            "/api/v1/register/", format="json", data=all_arguments)
        res_data = json.loads(res.content)

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Question.objects.count(), 2)
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(AnswerQuestion.objects.count(), 2)

        # Verify city preference fields
        self.assertEqual(len(res_data['answer_question']), 2)
        for k, v in self.answer_question_arguments["answer_question"][0].items():
            self.assertEqual(res_data['answer_question'][0][k], v)
        for k, v in self.answer_question_arguments["answer_question"][1].items():
            self.assertEqual(res_data['answer_question'][1][k], v)