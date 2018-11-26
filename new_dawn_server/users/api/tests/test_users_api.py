from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.test import TestCase
import datetime
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
    
    def test_register_fail_missing_fields(self):
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Account.objects.count(), 0)
        self.assertEqual(Profile.objects.count(), 0)
        self.assertHttpBadRequest(self.api_client.post("/api/v1/register/",
        format="json", data=self.register_arguments))
        self.assertEqual(User.objects.count(), 0)

    def test_register_success(self):
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Account.objects.count(), 0)
        self.assertEqual(Profile.objects.count(), 0)
        all_arguments = {
            **self.register_arguments, 
            **self.account_arguments, 
            **self.profile_arguments
        }
        res = self.api_client.post("/api/v1/register/",
        format="json", data=all_arguments)
        print([getattr(res, k) for k in dir(res)])
        # self.assertHttpCreated(self.api_client.post("/api/v1/register/",
        # format="json", data=all_arguments))

        # User, Account, Profile should be created together
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)

        # Verify User fields are populated
        user = User.objects.get(username="test-user")
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

