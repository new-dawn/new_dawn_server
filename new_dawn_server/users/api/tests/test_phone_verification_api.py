from django.test import Client, TestCase
from unittest.mock import patch, MagicMock


class PhoneVerifyTestCase(TestCase):

	@patch('new_dawn_server.users.resources.authy_api')
    def test_phone_verify_request(self, authy_api):
        client = Client()
        request_sms_response = MagicMock()
        request_sms_response.ok.return_value = True
        authy_api.users.request_sms.return_value = request_sms_response

        # Act
        response = client.post('/token/sms')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func, views.token_sms)
        authy_api.users.request_sms.assert_called_once_with(
            'fake',
            {'force': True}
        )
        request_sms_response.ok.assert_called_once()