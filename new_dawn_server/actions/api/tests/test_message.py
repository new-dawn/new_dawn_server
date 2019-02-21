import json

from django.contrib.auth.models import User
from django.test import TestCase
from new_dawn_server.actions.constants import ActionType, EntityType
from new_dawn_server.actions.models import UserAction
from tastypie.test import ResourceTestCaseMixin
from unittest.mock import patch


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

        self.message_argument = {
            "user_from": "1",
            "user_to": "2",
            "message": "How are you"
        }

    @patch("new_dawn_server.pusher.chat_service.ChatService.send")
    def test_message_user(self, send):
        res = self.api_client.post(
            "/api/v1/user_action/send_message/", format="json", data=self.message_argument
        )
        res_data = json.loads(res.content)
        # Check post response
        self.assertEqual(res_data["message"], "Message Sent")
        self.assertEqual(res_data["success"], True)
        # Check creation of objects
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(UserAction.objects.count(), 1)
        test_like_object = UserAction.objects.get(user_from__profile__user_id=1)
        self.assertEqual(test_like_object.action_type, ActionType.MESSAGE.value)
        self.assertEqual(test_like_object.entity_type, EntityType.NONE.value)
        self.assertEqual(test_like_object.entity_id, 1)
        self.assertEqual(test_like_object.user_to.username, "duck2")
        self.assertEqual(test_like_object.message, "How are you")
