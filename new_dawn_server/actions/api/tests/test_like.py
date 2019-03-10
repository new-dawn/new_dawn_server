import json

from django.contrib.auth.models import User
from django.test import TestCase
from new_dawn_server.actions.constants import ActionType, EntityType
from new_dawn_server.actions.models import UserAction
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
            "user_from": "1",
            "user_to": "2"
        }

    def test_like_user(self):
        res = self.api_client.post(
            "/api/v1/user_action/", format="json", data=self.like_argument
        )
        res_data = json.loads(res.content)
        # Check post response
        for k, v in self.like_argument.items():
            if k == "user_from" or k == "user_to":
                self.assertEqual(res_data[k]["resource_uri"], "/api/v1/user/" + self.like_argument[k] + "/")
            else:
                self.assertEqual(res_data[k], self.like_argument[k])
        # Check creation of objects
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(UserAction.objects.count(), 1)
        test_like_object = UserAction.objects.get(user_from__id=1)
        self.assertEqual(test_like_object.action_type, ActionType.LIKE.value)
        self.assertEqual(test_like_object.entity_type, EntityType.MAIN_IMAGE.value)
        self.assertEqual(test_like_object.entity_id, 1)
        self.assertEqual(test_like_object.user_to.username, "duck2")

    def test_match_user(self):
        self.api_client.post(
            "/api/v1/user_action/", format="json", data=self.like_argument
        )
        like_back_argument = {
            "action_type": ActionType.LIKE.value,
            "entity_id": 1,
            "entity_type": EntityType.MAIN_IMAGE.value,
            "user_from": "2",
            "user_to": "1"
        }
        self.api_client.post(
            "/api/v1/user_action/", format="json", data=like_back_argument
        )
        self.assertEqual(UserAction.objects.count(), 3)
        self.assertEqual(UserAction.objects.filter(action_type=ActionType.MATCH.value).count(), 1)
        match_obj = UserAction.objects.filter(action_type=ActionType.MATCH.value).first()
        self.assertEqual(match_obj.entity_id, 0)
        self.assertEqual(match_obj.user_to.id, 1)
        self.assertEqual(match_obj.user_from.id, 2)
        self.assertEqual(match_obj.entity_type, EntityType.NONE.value)



