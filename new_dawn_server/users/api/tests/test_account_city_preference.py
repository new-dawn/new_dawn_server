import json

from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from new_dawn_server.locations.models import CityPreference
from new_dawn_server.users.models import Account, Profile
from tastypie.test import ResourceTestCaseMixin


class AccountCreateTest(ResourceTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.register_arguments = {
            "first_name": "test",
            "last_name": "user",
            "username": "duck",
            "password": "test-pwd",
        }
        self.account_arguments = {
            "birthday": "1990-01-01",
            "phone_number": "+12345678900",
            "gender": "M",
        }
        self.profile_arguments = {
            "description": "nice",
            "employer": "MANMAN",
            "hometown": "NY",
            "job_title": "CEO",
            "profile_photo_url": "www",
            "school": "NYU",
            "smoke": "Socially",
        }
        self.city_preference_arguments = {"city_preference":
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

    def test_register_with_location(self):
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Account.objects.count(), 0)
        self.assertEqual(Profile.objects.count(), 0)
        self.assertEqual(CityPreference.objects.count(), 0)
        all_arguments = {
            **self.register_arguments,
            **self.profile_arguments,
            **self.account_arguments,
            **self.city_preference_arguments
        }
        res = self.api_client.post(
            "/api/v1/register/", format="json", data=all_arguments)
        res_data = json.loads(res.content)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(CityPreference.objects.count(), 2)
        user = User.objects.get(username="duck")
        # Verify account fields
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
            elif k == "city_preference":
                self.assertEqual(account.city_preference, v)
            else:
                self.assertEqual(getattr(account, k), v)

        # Verify Profile fields are populated
        profile = Profile.objects.get(user=user)
        for k, v in self.profile_arguments.items():
            self.assertEqual(getattr(profile, k), v)

        # Verify city preference fields
        self.assertEqual(len(res_data['city_preference']), 2)
        for k, v in self.city_preference_arguments["city_preference"][0].items():
            self.assertEqual(res_data['city_preference'][0][k], v)
        for k, v in self.city_preference_arguments["city_preference"][1].items():
            self.assertEqual(res_data['city_preference'][1][k], v)

    def test_get_account_location(self):
        all_arguments = {
            **self.register_arguments,
            **self.profile_arguments,
            **self.account_arguments,
            **self.city_preference_arguments
        }
        res = self.api_client.post(
            "/api/v1/register/", format="json", data=all_arguments)
        res_data = json.loads(res.content)
        api_credential = self.create_apikey(username=res_data["username"], api_key=res_data["token"])
        res = self.api_client.get("/api/v1/account/", format="json", authentication=api_credential)
        res_data = json.loads(res.content)
        for location in range(0, 2):
            for k, v in self.city_preference_arguments['city_preference'][location].items():
                self.assertEqual(res_data['objects'][0]['city_preference'][location][k], v)
