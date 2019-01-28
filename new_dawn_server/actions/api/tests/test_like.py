import json

from django.contrib.auth.models import User
from django.test import TestCase
from new_dawn_server.actions.constants import ActionType, EntityType
from new_dawn_server.actions.models import UserAction
from new_dawn_server.users.models import Account
from tastypie.test import ResourceTestCaseMixin


class UserActionTest(ResourceTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.user1_aruguments = {
            "first_name": "test",
            "last_name": "user",
            "username": "duck",
            "password": "test-pwd",
            "birthday": "1990-01-01",
            "phone_number": "+12345678900",
            "gender": "M",
            "description": "nice",
            "employer": "MANMAN",
            "hometown": "NY",
            "job_title": "CEO",
            "profile_photo_url": "www",
            "school": "NYU",
            "smoke": "Socially",
            "city_preference":
                [
                    {
                        "city": "New York",
                        "country": "US",
                        "state": "NY"
                    },
                    {
                        "city": "Salt Lake City",
                        "country": "US",
                        "state": "UT"
                    }
                ]
        }
        self.user2_arguments = {
            "first_name": "test2",
            "last_name": "user2",
            "name": "goodgirl",
            "username": "duck2",
            "password": "test-pwd2",
            "birthday": "1990-01-01",
            "phone_number": "+12345678900",
            "gender": "M",
            "description": "nice",
            "employer": "MANMAN",
            "hometown": "NY",
            "job_title": "CEO",
            "profile_photo_url": "www",
            "school": "NYU",
            "smoke": "Socially",
            "city_preference":
                [
                    {
                        "city": "New York",
                        "country": "US",
                        "state": "NY"
                    },
                    {
                        "city": "Salt Lake City",
                        "country": "US",
                        "state": "UT"
                    }
                ]
        }
        self.api_client.post(
            "/api/v1/register/", format="json", data=self.user1_aruguments)
        self.api_client.post(
            "/api/v1/register/", format="json", data=self.user2_arguments)

        self.like_argument = {
            "action_type": ActionType.LIKE.value,
            "entity_id": 1,
            "entity_type": EntityType.MAIN_IMAGE.value,
            "user_account_from": "/api/v1/account/1/",
            "user_account_to": "/api/v1/account/2/"
        }

    def test_like_user(self):
        res = self.api_client.post(
            "/api/v1/user_action/", format="json", data=self.like_argument
        )
        res_data = json.loads(res.content)
        self.assertEqual(Account.objects.count(), 2)
        self.assertEqual(UserAction.objects.count(), 1)
        test_like_object = UserAction.objects.get(user_account_from__profile__user_id=1)
        self.assertEqual(test_like_object.action_type, ActionType.LIKE.value)
        self.assertEqual(test_like_object.entity_type, EntityType.MAIN_IMAGE.value)
        self.assertEqual(test_like_object.entity_id, 1)
        self.assertEqual(test_like_object.user_account_to.name, "test2_user2")