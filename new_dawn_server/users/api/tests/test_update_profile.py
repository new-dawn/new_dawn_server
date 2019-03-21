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
            "degree": "high school",
            "description": "nice",
            "drink": "NO",
            "employer": "MANMAN",
            "hometown": "NY",
            "job_title": "CEO",
            "profile_photo_url": "www",
            "school": "NYU",
            "smoke": "Socially",
        }

        self.all_arguments = {
            **self.register_arguments,
            **self.account_arguments,
            **self.profile_arguments
        }
        self.api_client.post(
            "/api/v1/register/", format="json", data=self.all_arguments)
        self.self_id = User.objects.first().id

    def test_register_update_user(self):
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)
        register_arguments_2 = {
            "first_name": "test-update",
            "username": "test-user",
            "last_name": "123",
            "password": "test-pwd",
            "id": self.self_id,
        }
        account_arguments_2 = {
            "birthday": "1990-01-01",
            "phone_number": "+12345678900",
            "gender": "F",
        }
        profile_arguments_2 = {
            "degree": "high school",
            "description": "nice22222",
            "drink": "NO",
            "employer": "MANMAN",
            "hometown": "NY",
            "job_title": "CEO",
            "profile_photo_url": "www",
            "school": "NYU",
            "smoke": "Socially",
        }

        all_arguments_2 = {
            **register_arguments_2,
            **account_arguments_2,
            **profile_arguments_2
        }
        all_arguments_2 = {
            "objects": [all_arguments_2]
        }

        self.api_client.put(
            "/api/v1/register/", format="json", data=all_arguments_2)

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(User.objects.first().first_name, "test-update")
        self.assertEqual(Account.objects.first().gender, "F")
        self.assertEqual(Profile.objects.first().description, "nice22222")
        self.assertEqual(Profile.objects.first().degree, "high school")

        res = self.api_client.get("/api/v1/profile/", format="json")
        res_data = json.loads(res.content)
        user_data = res_data["objects"][0]
        self.assertEqual(user_data["degree"], "high school")
        self.assertEqual(user_data["description"], "nice22222")
