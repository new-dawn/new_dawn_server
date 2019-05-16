import json

from django.test import TestCase
from new_dawn_server.users.models import User
from tastypie.test import ResourceTestCaseMixin
from unittest.mock import patch, MagicMock, PropertyMock


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
        self.user_id = res_body["username"]

    def test_authenticate(self):
        with patch(
            "new_dawn_server.pusher.notification_service.NotificationService._get_instance_id_and_secret_key",
            return_value=["instance", "key"]
        ), patch(
             "new_dawn_server.pusher.notification_service.NotificationService.send_notification",
            return_value=None
        ), patch(
             "new_dawn_server.pusher.notification_service.NotificationService.beams_auth",
            return_value={
                "token": "XXX"
            }
        ):
            self.assertEqual(User.objects.count(), 1)
            # Positive: authentication successful
            res = self.api_client.get("/api/v1/user/notification/authenticate/?user_id=test-user")
            res_body = json.loads(res.content)
            self.assertIn("token", res_body)
            self.assertEqual(res_body["token"], "XXX")
            # Negative: authentication fails
            res = self.api_client.get("/api/v1/user/notification/authenticate/?user_id=1")
            # No content response
            self.assertEqual(res.status_code, 204)