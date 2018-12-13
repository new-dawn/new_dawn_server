import json

from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from new_dawn_server.locations.models import CityPreference
from new_dawn_server.users.models import Account
from tastypie.test import ResourceTestCaseMixin


class AccountCreateTest(ResourceTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.user_arguments = {
            "first_name": "junlin",
            "last_name": "liu",
            "username": "duck",
            "password": "123",
        }
        self.account_arguments = {
            "birthday": "1990-01-01",
            "phone_number": "+12345678900",
            "gender": "M",
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

    def test_account_with_location(self):
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Account.objects.count(), 0)
        self.assertEqual(CityPreference.objects.count(), 0)
        all_arguments = {
            **self.city_preference_arguments,
            **self.user_arguments,
            **self.account_arguments,
        }
        res = self.api_client.post(
            "/api/v1/account/", format="json", data=all_arguments)
        res_data = json.loads(res.content)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(CityPreference.objects.count(), 2)
        user = User.objects.get(username="duck")
        # Verify account fields
        for k, v in self.user_arguments.items():
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

        # Verify city preference fields
        self.assertEqual(len(res_data['city_preference']), 2)
        for k, v in self.city_preference_arguments["city_preference"][0].items():
            self.assertEqual(res_data['city_preference'][0][k], v)
        for k, v in self.city_preference_arguments["city_preference"][1].items():
            self.assertEqual(res_data['city_preference'][1][k], v)