from django.contrib.auth.models import User
from django.test import TestCase
from new_dawn_server.questions.models import AnswerQuestion, Question


class QuestionTest(TestCase):
    def setUp(self):
        Question.objects.create(
            question="How are you doing?",
            sample_answer="Very Good",
        )

    def test_question(self):
        test_question_case = Question.objects.first()
        self.assertEqual(test_question_case.question, "How are you doing?")
        self.assertEqual(test_question_case.sample_answer, "Very Good")


class AnswerQuestionTest(TestCase):
    def setUp(self):
        Question.objects.create(
            question="How are you doing?",
            sample_answer="Very Good",
        )

        AnswerQuestion.objects.create(
            answer="Good Good Good",
            order=1,
            question=Question.objects.first(),
            user=User.objects.create()
        )

    def test_get_QA_from_user(self):
        test_user = User.objects.first()
        test_qa = AnswerQuestion.objects.get(user=test_user)
        self.assertEqual(test_qa.question.question, "How are you doing?")
        self.assertEqual(test_qa.answer, "Good Good Good")
        self.assertEqual(test_qa.order, 1)
        self.assertEqual(test_qa.question.sample_answer, "Very Good")
