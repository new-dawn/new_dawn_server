import json

from django.contrib.auth.models import User
from django.test import TestCase
from new_dawn_server.questions.models import AnswerQuestion, Question
from tastypie.test import ResourceTestCaseMixin


class QuestionTest(ResourceTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.question_argument = {
            "question": "How are you doing?",
            "sample_answer": "Pretty Good",
        }
        self.answer_question_argument = {
            "order": 1,
            "answer": "Good Good",
        }
        self.register_argument = {
            "first_name": "test",
            "last_name": "user",
            "username": "test-user",
            "password": "test-pwd",
        }
        self.api_client.post(
            "/api/v1/register/", format="json", data=self.register_argument)

    def test_question_post_resource(self):
        self.assertEqual(Question.objects.count(), 0)
        res = self.api_client.post(
            "/api/v1/question/", format="json", data=self.question_argument)
        res_data = json.loads(res.content)
        for k, v in self.question_argument.items():
            self.assertTrue(k in res_data)
            self.assertTrue(v, res_data[k])
        self.assertEqual(Question.objects.count(), 1)
        # Verify question fields are populated
        question = Question.objects.first()
        for k, v in self.question_argument.items():
            self.assertEqual(getattr(question, k), v)

    def test_question_get_resource(self):
        self.api_client.post(
            "/api/v1/question/", format="json", data=self.question_argument)
        res = self.api_client.get("/api/v1/question/", format="json")
        res_data = json.loads(res.content)
        # Verify all the data gets populated
        for k, v in self.question_argument.items():
            self.assertTrue(k in res_data['objects'][0])
            self.assertTrue(v, res_data['objects'][0][k])

    def test_answer_question_post_resource(self):
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Question.objects.count(), 0)
        self.assertEqual(AnswerQuestion.objects.count(), 0)
        all_arguments = {
            **self.answer_question_argument,
            "user": "/api/v1/user/1/",
            "question": "/api/v1/question/1/"
        }
        self.api_client.post(
            "/api/v1/question/", format="json", data=self.question_argument)

        res = self.api_client.post(
            "/api/v1/answer_question/", format="json", data=all_arguments)
        res_data = json.loads(res.content)

        for k, v in all_arguments.items():
            self.assertTrue(k in res_data)
            # Already tested user and question
            if k == "user":
                no_password_args = self.register_argument
                no_password_args.pop("password", None)
                self.assertTrue(no_password_args.items() < res_data["user"].items())
            elif k == "question":
                self.assertTrue(self.question_argument.items() < res_data["question"].items())
            else:
                self.assertEqual(v, res_data[k])

        # User, Question, AnswerQuestion should be created together
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(AnswerQuestion.objects.count(), 1)

    def test_answer_question_get_resource(self):

        all_arguments = {
            **self.answer_question_argument,
            "user": "/api/v1/user/1/",
            "question": "/api/v1/question/1/"
        }
        self.api_client.post(
            "/api/v1/question/", format="json", data=self.question_argument)

        self.api_client.post(
            "/api/v1/answer_question/", format="json", data=all_arguments)

        res = self.api_client.get("/api/v1/answer_question/", format="json")
        res_data = json.loads(res.content)

        # Verify Data were posted and getted correctly
        for k, v in self.register_argument.items():
            if k == "password":
                continue
            self.assertTrue(k in res_data['objects'][0]['user'])
            self.assertTrue(v, res_data['objects'][0]['user'][k])
        for k, v in self.question_argument.items():
            self.assertTrue(k in res_data['objects'][0]['question'])
            self.assertTrue(v, res_data['objects'][0]['question'][k])
        for k, v in self.answer_question_argument.items():
            self.assertTrue(k in res_data['objects'][0])
            self.assertTrue(v, res_data['objects'][0][k])
