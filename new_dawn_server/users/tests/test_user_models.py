import datetime
from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from new_dawn_server.questions.models import AnswerQuestion, Question
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
        Account.objects.create(
            birthday="1996-01-01",
            gender="M",
            phone_number="+14004004400",
            name="testuser",
            user=User.objects.create(username="101010")
        )
        self.profile = Profile.objects.create(
            account=Account.objects.get(name="testuser"),
            degree="high school",
            description="Good Boy",
            drink="NO",
            employer="ManMan",
            height=Decimal(180.00),
            hometown="Chongqing",
            job_title="Analyst",
            profile_photo_url="manman.com",
            school="NYU",
            smoke="Socially",
            user=User.objects.get(username="101010")
        )
        Question.objects.create(
            question="How are you doing?",
            sample_answer="Very Good",
        )
        # Multiple answers attached to one profile
        AnswerQuestion.objects.create(
            answer="Good Good Good",
            order=1,
            profile=self.profile,
            question=Question.objects.first(),
            user=User.objects.get(username="101010")
        )
        AnswerQuestion.objects.create(
            answer="Good Good Bad",
            order=2,
            profile=self.profile,
            question=Question.objects.first(),
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
        # Access reverse relationship from profile to answer questions via _set suffix
        test_answer_questions = test_user_profile.answerquestion_set.all()
        self.assertEqual(test_answer_questions[0].question.question, "How are you doing?")
        self.assertEqual(test_answer_questions[0].order, 1)
        self.assertEqual(test_answer_questions[0].answer, "Good Good Good")
        self.assertEqual(test_answer_questions[1].order, 2)
        self.assertEqual(test_answer_questions[1].answer, "Good Good Bad")

    def test_profile_boolean_fields(self):
        return

    def test_profile_char_fields(self):
        test_user_account = Account.objects.get(name="testuser")
        test_user_profile = Profile.objects.get(account=test_user_account)
        self.assertEqual(test_user_profile.description, "Good Boy")
        self.assertEqual(test_user_profile.employer, "ManMan")
        self.assertEqual(test_user_profile.hometown, "Chongqing")
        self.assertEqual(test_user_profile.job_title, "Analyst")
        self.assertEqual(test_user_profile.profile_photo_url, "manman.com")
        self.assertEqual(test_user_profile.school, "NYU")
        self.assertEqual(test_user_profile.drink, "NO")
        self.assertEqual(test_user_profile.smoke, "Socially")
        self.assertEqual(test_user_profile.degree, "high school")

    def test_profile_decimal_fields(self):
        test_user_account = Account.objects.get(name="testuser")
        test_user_profile = Profile.objects.get(account=test_user_account)
        self.assertEqual(test_user_profile.height, 180.00)
