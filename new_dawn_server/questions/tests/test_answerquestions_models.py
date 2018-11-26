from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from new_dawn_server.questions.models import AnswerQuestions, Questions
from new_dawn_server.users.models import Account, Profile



class QuestionTest(TestCase):
    def setUp(self):
        Questions.objects.create(
            question="How are you doing?",
            sample_answer="Very Good",
        )

    def test_question(self):
        test_question_case = Questions.objects.first()
        self.assertEqual(test_question_case.question, "How are you doing?")
        self.assertEqual(test_question_case.sample_answer, "Very Good")

class AnswerQuestionTest(TestCase):
    def setUp(self):
        Account.objects.create(
            birthday="1996-01-01",
            gender="M",
            phone_number="+14004004400",
            name="testuser",
            user=User.objects.create()
        )
        Profile.objects.create(
            account=Account.objects.get(name="testuser"),
            city_preference="New York",
            description="Good Boy",
            employer="ManMan",
            height=Decimal(180.00),
            hometown="Chongqing",
            job_title="Analyst",
            profile_photo_url="manman.com",
            school="NYU",
            smoke="True"
        )
        Questions.objects.create(
            question="How are you doing?",
            sample_answer="Very Good",
        )
        AnswerQuestions.objects.create(
            answer="Good Good Good",
            order = 1,
            question=Questions.objects.first(),
            user=Profile.objects.first()
        )

    def test_get_QA_from_user(self):
        test_user = Profile.objects.first()
        test_qa = AnswerQuestions.objects.get(user=test_user)
        self.assertEqual(test_qa.question.question, "How are you doing?")
        self.assertEqual(test_qa.answer, "Good Good Good")
        self.assertEqual(test_qa.order, 1)
        self.assertEqual(test_qa.question.sample_answer, "Very Good")