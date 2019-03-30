import json

from django.test import TestCase
from new_dawn_server.users.models import User
from tastypie.test import ResourceTestCaseMixin


# MultiAuthentication works when any of its authentication method is fulfilled
class NotificationTest(ResourceTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.register_arguments = {
            "first_name": "test",
            "last_name": "user",
            "username": "test-user",
            "password": "test-pwd",
        }
        res = self.api_client.post(
            "/api/v1/register/", format="json", data=self.register_arguments)
        res_body = json.loads(res.content)
        self.user_id = res_body["id"]

    def test_authenticate(self):
        self.assertEqual(User.objects.count(), 1)
        # Positive: authentication successful
        res = self.api_client.get("/api/v1/user/notification/authenticate/?user_id=1")
        res_body = json.loads(res.content)
        self.assertIn("token", res_body)
        # Negative: authentication fails
        res = self.api_client.get("/api/v1/user/notification/authenticate/?user_id=10")
        # No content response
        self.assertEqual(res.status_code, 204)