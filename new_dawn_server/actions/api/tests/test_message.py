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
        self.user1_arguments = {
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
        self.user3_arguments = {
            "first_name": "test3",
            "last_name": "user3",
            "name": "goodgirl",
            "username": "ziyi3",
            "password": "test-pwd3",
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
            "/api/v1/register/", format="json", data=self.user1_arguments)
        self.api_client.post(
            "/api/v1/register/", format="json", data=self.user2_arguments)
        self.api_client.post(
            "/api/v1/register/", format="json", data=self.user3_arguments)

        self.message_argument = {
            "user_from": "1",
            "user_to": "2",
            "message": "How are you"
        }
        self.message_argument_2 = {
            "user_from": "2",
            "user_to": "1",
            "message": "I'm good"
        }
        self.message_argument_3 = {
            "user_from": "2",
            "user_to": "3",
            "message": "Nice to meet you"
        }

    @patch("new_dawn_server.pusher.chat_service.ChatService.send")
    def test_message_user(self, send):
        res_1 = self.api_client.post(
            "/api/v1/user_action/send_message/", format="json", data=self.message_argument
        )
        res_2 = self.api_client.post(
            "/api/v1/user_action/send_message/", format="json", data=self.message_argument_2
        )
        res_3 = self.api_client.post(
            "/api/v1/user_action/send_message/", format="json", data=self.message_argument_3
        )
        res_all = [res_1, res_2, res_3]
        for res in res_all:
            res_data = json.loads(res.content)
            # Check post response
            self.assertEqual(res_data["message"], "Message Sent")
            self.assertEqual(res_data["success"], True)

        # Check creation of objects
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(UserAction.objects.count(), 3)
        # Test all messages sent by user 1
        test_message_object = UserAction.objects.get(user_from__id=1)
        self.assertEqual(test_message_object.action_type, ActionType.MESSAGE.value)
        self.assertEqual(test_message_object.entity_type, EntityType.NONE.value)
        self.assertEqual(test_message_object.entity_id, 1)
        self.assertEqual(test_message_object.user_to.username, "duck2")
        self.assertEqual(test_message_object.message, "How are you")
        # Test GET API for all messages between user 1 and user 2
        res = self.api_client.get(
            "/api/v1/user_action/get_messages/?user_from=1&user_to=2", format="json"
        )
        res_data = json.loads(res.content)
        self.assertEqual(len(res_data["objects"]), 2)
        self.assertEqual(res_data["objects"][0]["user_from"], 1)
        self.assertEqual(res_data["objects"][0]["user_to"], 2)
        self.assertEqual(res_data["objects"][0]["message"], "How are you")
        self.assertEqual(res_data["objects"][1]["user_from"], 2)
        self.assertEqual(res_data["objects"][1]["user_to"], 1)
        self.assertEqual(res_data["objects"][1]["message"], "I'm good")

        # Test GET API for all messages between user 1 and user 2
        res = self.api_client.get(
            "/api/v1/user_action/get_messages/?user_from=1&user_to=2&only_last=1", format="json"
        )
        res_data = json.loads(res.content)
        self.assertEqual(len(res_data["objects"]), 1)
        self.assertEqual(res_data["objects"][0]["user_from"], 2)
        self.assertEqual(res_data["objects"][0]["user_to"], 1)
        self.assertEqual(res_data["objects"][0]["message"], "I'm good")

        res = self.api_client.get(
            "/api/v1/user_action/get_messages/?user_from=2&user_to=3", format="json"
        )
        res_data = json.loads(res.content)
        self.assertEqual(len(res_data["objects"]), 1)
        self.assertEqual(res_data["objects"][0]["user_from"], 2)
        self.assertEqual(res_data["objects"][0]["user_to"], 3)
        self.assertEqual(res_data["objects"][0]["message"], "Nice to meet you")
