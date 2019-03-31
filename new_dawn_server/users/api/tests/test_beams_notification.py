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
        self.user_id = res_body["id"]

    @patch("new_dawn_server.pusher.notification_service.NotificationService")
    def test_authenticate(self, mock_service):
        mock_service.beams_client.beams_auth.return_value = {
            "token": "XXXXXXXXXXXXXX"
        }
        self.assertEqual(User.objects.count(), 1)
        # Positive: authentication successful
        res = self.api_client.get("/api/v1/user/notification/authenticate/?user_id=1")
        res_body = json.loads(res.content)
        self.assertIn("token", res_body)
        type(mock_service.beams_client.beams_auth).status_code = PropertyMock(return_value=204)
        # Negative: authentication fails
        res = self.api_client.get("/api/v1/user/notification/authenticate/?user_id=10")
        # No content response
        self.assertEqual(res.status_code, 204)