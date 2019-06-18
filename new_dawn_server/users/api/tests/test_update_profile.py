import datetime
import json

from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from new_dawn_server.medias.models import Image
from new_dawn_server.questions.models import AnswerQuestion
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
            "answer_question":
                [
                    {
                        "question": "how are you",
                        "order": 1,
                        "answer": "good",
                    },
                    {
                        "question": "How do you do",
                        "order": 2,
                        "answer": "do do"
                    }
                ]
        }

        self.all_arguments = {
            **self.register_arguments,
            **self.account_arguments,
            **self.profile_arguments
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
                ],
            "answer_question":
                [
                    {
                        "question": "how are you",
                        "order": 1,
                        "answer": "good",
                    },
                    {
                        "question": "How do you do",
                        "order": 2,
                        "answer": "do do"
                    }
                ]
        }

        # Post questions before answer
        self.pre_defined_question_arguments = {
            "question": "how are you",
            "sample_answer": "ummm",
            "user_defined": False
        }
        self.api_client.post("/api/v1/question/", format="json", data=self.pre_defined_question_arguments)
        self.pre_defined_question_arguments = {
            "question": "How do you do",
            "sample_answer": "ummm",
            "user_defined": False
        }
        self.api_client.post("/api/v1/question/", format="json", data=self.pre_defined_question_arguments)

    def test_register_update_user(self):
        self.api_client.post(
            "/api/v1/register/", format="json", data=self.all_arguments)
        self.api_client.post(
            "/api/v1/register/", format="json", data=self.user2_arguments)

        self.test_data = {
            "caption": "good",
            "order": 1,
            "user": "/api/v1/user/1/",
        }
        with open("media/images/test.png", "rb") as photo_file:
            test_data_json = json.dumps(self.test_data)
            full_data = {
                "data": test_data_json,
                "media": photo_file,
            }
            response = self.client.post(
                '/api/v1/image/',
                data=full_data,
            )
        self.assertEqual(Image.objects.count(), 1)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(Account.objects.count(), 2)
        self.assertEqual(Profile.objects.count(), 2)
        self.assertEqual(AnswerQuestion.objects.count(), 4)

        # Test if the review_status can be carried over to the new profile
        p = Profile.objects.get(user__id=1)
        p.review_status = 4
        p.save()

        register_arguments_2 = {
            "first_name": "test-change",
            "username": "test-user",
            "last_name": "123",
            "password": "test-pwd",
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
            **profile_arguments_2,
        }

        self.api_client.put(
            "/api/v1/register/1/", format="json", data=all_arguments_2)

        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(Account.objects.count(), 2)
        self.assertEqual(Profile.objects.count(), 2)
        # Question Answers are kept after update
        self.assertEqual(AnswerQuestion.objects.count(), 4)
        # Images are kept after update
        self.assertEqual(Image.objects.count(), 1)
        self.assertEqual(User.objects.get(id=1).first_name, "test-change")
        self.assertEqual(Account.objects.get(user_id=1).gender, "F")
        self.assertEqual(Profile.objects.get(user_id=1).description, "nice22222")
        self.assertEqual(Profile.objects.get(user_id=1).degree, "high school")

        res = self.api_client.get("/api/v1/profile/", format="json")
        res_data = json.loads(res.content)
        user_data = res_data["objects"][1]
        self.assertEqual(user_data["degree"], "high school")
        self.assertEqual(user_data["description"], "nice22222")
        # Review status shouldn't change
        self.assertEqual(res_data["objects"][1]["review_status"], 4)
        # Confirm other users' information not been affected
        user_data_2 = res_data["objects"][0]
        self.assertEqual(user_data_2["user"]["first_name"], "test2")
        self.assertEqual(user_data_2["description"], "nice")

        # Get profile should not get images from updated profile
        self.assertEqual(len(user_data["images"]), 0)
        self.assertEqual(len(user_data_2["images"]), 0)

        # Updated image will link to updated profiles
        with open("media/images/test.png", "rb") as photo_file:
            test_data_json = json.dumps(self.test_data)
            full_data = {
                "data": test_data_json,
                "media": photo_file,
            }
            response = self.client.post(
                '/api/v1/image/',
                data=full_data,
            )
        res = self.api_client.get("/api/v1/profile/", format="json")
        res_data = json.loads(res.content)
        user_data = res_data["objects"][1]
        # You can only get one image from this profile after update
        self.assertEqual(Image.objects.count(), 2)
        self.assertEqual(len(user_data["images"]), 1)