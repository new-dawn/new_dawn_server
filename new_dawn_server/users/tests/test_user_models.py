import datetime
from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from new_dawn_server.questions.models import AnswerQuestions, Questions
from new_dawn_server.users.models import Account, Profile


class AccountTest(TestCase):
    def setUp(self):
        Account.objects.create(
            birthday="1996-01-01",
            gender="M",
            phone_number="+14004004400",
            name="testuser",
            user=User.objects.create()
        )

    def test_account_basic_info(self):
        test_user_account = Account.objects.get(name="testuser")
        self.assertEqual(test_user_account.name, "testuser")
        self.assertEqual(test_user_account.gender, "M")
        self.assertEqual(test_user_account.get_gender_display(), "Male")
        self.assertEqual(test_user_account.birthday, datetime.date(1996, 1, 1))

    def test_account_phone_number(self):
        test_user_acount = Account.objects.get(name="testuser")
        self.assertEqual(test_user_acount.phone_number.as_international, "+1 400-400-4400")
        self.assertEqual(test_user_acount.phone_number.as_national, "(400) 400-4400")
        self.assertEqual(test_user_acount.phone_number.as_e164, "+14004004400")
        self.assertEqual(test_user_acount.phone_number.as_rfc3966, "tel:+1-400-400-4400")


class ProfileTest(TestCase):
    def setUp(self):
        user = User.objects.create()
        Account.objects.create(
            birthday="1996-01-01",
            gender="M",
            phone_number="+14004004400",
            name="testuser",
            user=User.objects.create(username="101010")
        )
        Questions.objects.create(
            question="How are you doing?",
            sample_answer="Very Good",
        )
        AnswerQuestions.objects.create(
            answer="Good Good Good",
            order=1,
            question=Questions.objects.first(),
            user=User.objects.get(username="101010")
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
            smoke="True",
            answer_questions=AnswerQuestions.objects.first()
            user=User.objects.get(username="101010")
        )

    def test_profile_account_relationship(self):
        test_user_account = Account.objects.get(name="testuser")
        test_user_profile = Profile.objects.get(account=test_user_account)
        self.assertEqual(test_user_account.name, test_user_profile.account.name)
        self.assertEqual(test_user_account.gender, test_user_profile.account.gender)
        self.assertEqual(test_user_account.get_gender_display(), test_user_profile.account.get_gender_display())
        self.assertEqual(test_user_account.birthday, test_user_profile.account.birthday)

    def test_profile_answer_questions(self):
        test_user_account = Account.objects.get(name="testuser")
        test_user_profile = Profile.objects.get(account=test_user_account)
        test_questions = test_user_profile.answer_questions
        self.assertEqual(test_questions.question.question, "How are you doing?")
        self.assertEqual(test_questions.order, 1)
        self.assertEqual(test_questions.answer, "Good Good Good")

    def test_profile_boolean_fields(self):
        test_user_account = Account.objects.get(name="testuser")
        test_user_profile = Profile.objects.get(account=test_user_account)
        self.assertEqual(test_user_profile.smoke, True)

    def test_profile_char_fields(self):
        test_user_account = Account.objects.get(name="testuser")
        test_user_profile = Profile.objects.get(account=test_user_account)
        self.assertEqual(test_user_profile.city_preference, "New York")
        self.assertEqual(test_user_profile.description, "Good Boy")
        self.assertEqual(test_user_profile.employer, "ManMan")
        self.assertEqual(test_user_profile.hometown, "Chongqing")
        self.assertEqual(test_user_profile.job_title, "Analyst")
        self.assertEqual(test_user_profile.profile_photo_url, "manman.com")
        self.assertEqual(test_user_profile.school, "NYU")

    def test_profile_decimal_fields(self):
        test_user_account = Account.objects.get(name="testuser")
        test_user_profile = Profile.objects.get(account=test_user_account)
        self.assertEqual(test_user_profile.height, 180.00)
