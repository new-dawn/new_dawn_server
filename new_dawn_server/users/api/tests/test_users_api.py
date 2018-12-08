import datetime
import json

from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from new_dawn_server.users.models import Account
from new_dawn_server.users.models import Profile
from tastypie.test import ResourceTestCaseMixin


class UserRegisterTest(ResourceTestCaseMixin, TestCase):
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
            "city_preference": "New York",
            "description": "nice",
            "employer": "MANMAN",
            "hometown": "NY",
            "job_title": "CEO",
            "profile_photo_url": "www",
            "school": "NYU",
            "smoke": True,
        }

    def test_register_success(self):
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Account.objects.count(), 0)
        self.assertEqual(Profile.objects.count(), 0)
        all_arguments = {
            **self.register_arguments,
            **self.account_arguments,
            **self.profile_arguments
        }
        res = self.api_client.post(
            "/api/v1/register/", format="json", data=all_arguments)

        user = User.objects.get(username="test-user")
        res_data = json.loads(res.content)
        res_data["username"] = self.register_arguments["username"]
        res_data["token"] = user.api_key.key

        # User, Account, Profile should be created together
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)

        # Verify User fields are populated
        for k, v in self.register_arguments.items():
            if k == "password":
                self.assertTrue(check_password(v, getattr(user, k)))
            else:
                self.assertEqual(getattr(user, k), v)

        # Verify Account fields are populated
        account = Account.objects.get(user=user)
        for k, v in self.account_arguments.items():
            if k == "birthday":
                self.assertEqual(getattr(account, k).strftime("%Y-%m-%d"), v)
            else:
                self.assertEqual(getattr(account, k), v)

                # Verify Profile fields are populated
        profile = Profile.objects.get(user=user)
        for k, v in self.profile_arguments.items():
            self.assertEqual(getattr(profile, k), v)

    def test_login_success(self):
        all_arguments = {
            **self.register_arguments,
            **self.account_arguments,
            **self.profile_arguments
        }
        login_arguments = {
            "username": self.register_arguments["username"],
            "password": self.register_arguments["password"],
        }

        # Register a new account
        self.api_client.post(
            "/api/v1/register/", format="json", data=all_arguments)

        # Check login success
        res = self.api_client.post(
            "/api/v1/user/login/", format="json", data=login_arguments)

        # Return success message and api-key
        res_data = json.loads(res.content)
        user = User.objects.get(username="test-user")
        self.assertEqual(res_data["success"], True)
        self.assertEqual(res_data["username"], self.register_arguments["username"])
        self.assertEqual(res_data["token"], user.api_key.key)

    def test_user_profile_get(self):
        all_arguments = {
            **self.register_arguments,
            **self.account_arguments,
            **self.profile_arguments
        }
        self.api_client.post(
            "/api/v1/register/", format="json", data=all_arguments)

        res = self.api_client.get("/api/v1/profile/", format="json", data={"username": "test-user"})
        res_data = json.loads(res.content)
        for k, v in self.profile_arguments.items():
            self.assertEqual(res_data['objects'][0][k], v)


class ProfileQuestionTest(ResourceTestCaseMixin, TestCase):
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
            "city_preference": "New York",
            "description": "nice",
            "employer": "MANMAN",
            "hometown": "NY",
            "job_title": "CEO",
            "profile_photo_url": "www",
            "school": "NYU",
            "smoke": True,
        }
        self.question_argument_1 = {
            "question": "How are you doing?",
            "sample_answer": "Pretty Good",
        }
        self.question_argument_2 = {
            "question": "Good?",
            "sample_answer": "Good",
        }
        self.question_argument_3 = {
            "question": "Good good?",
            "sample_answer": "good good",
        }

        all_arguments = {
            **self.register_arguments,
            **self.account_arguments,
            **self.profile_arguments
        }
        self.api_client.post(
            "/api/v1/register/", format="json", data=all_arguments)
        self.api_client.post(
            "/api/v1/question/", format="json", data=self.question_argument_1)
        self.api_client.post(
            "/api/v1/question/", format="json", data=self.question_argument_2)
        self.api_client.post(
            "/api/v1/question/", format="json", data=self.question_argument_3)

    def test_get_all_profiles_questions(self):

        for i in range(1, 4):
            all_arguments = {
                "order": i,
                "answer": "niu",
                "user": "/api/v1/user/1/",
                "question": f"/api/v1/question/{i}/",
            }
            self.api_client.post(
                "/api/v1/answer_question/", format="json", data=all_arguments
            )
        res = self.api_client.get("/api/v1/profile/", format="json")
        res_data = json.loads(res.content)
        for k, v in res_data['objects'][0].items():
            if k == "user":
                self.assertTrue(v['username'] == "test-user")
            if k == "answer_question":
                self.assertTrue(len(v), 3)
                question_order = 1
                for each in v:
                    self.assertTrue(each['answer'], "niu")
                    self.assertTrue(each['order'], question_order)
