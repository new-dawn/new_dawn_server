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
            "phone_number": "1234567890",
            "gender": "M",
        }
        self.profile_arguments = {
            "job_title": "CEO",
            "smoke": True,
            "gender": "M",
        }
    
    def test_register_fail_missing_fields(self):
        self.assertEqual(User.objects.count(), 0)
        self.assertHttpBadRequest(self.api_client.post('/api/v1/register/',
        format='json', data=self.register_arguments))
        self.assertEqual(User.objects.count(), 0)

    def test_register_success(self):
        self.assertEqual(User.objects.count(), 0)
        all_arguments = {
            **self.register_arguments, 
            **self.account_arguments, 
            **self.profile_arguments
        }

        res = self.api_client.post('/api/v1/register/',
            format='json', data=all_arguments)
        #self.assertHttpCreated(self.api_client.post('/api/v1/register/',
        #format='json', data=all_arguments))
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)

        # Verify User fields are populated
        user = User.objects.get(username='test-user')

