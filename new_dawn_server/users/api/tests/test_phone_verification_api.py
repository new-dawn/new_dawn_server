from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin
from unittest.mock import patch, MagicMock


class PhoneVerifyTestCase(ResourceTestCaseMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.request_args_empty = {}
        self.request_args = {
            "phone_number": "1111111111",
            "country_code": "1",
            "via": "sms",
        }
        self.authenticate_args = {
            "phone_number": "1111111111",
            "country_code": "1",
            "verification_code": "testtoken",
        }

    # For test purpose, we don't send the actual request with authy api
    # Instead we mock its expected responses and verify we can handle them correctly
    @patch('new_dawn_server.users.api.resources.authy_api')
    def test_phone_verify_request(self, authy_api):
        authy_api.phones.verification_start = MagicMock()

        # Empty request args
        response = self.api_client.post(
            "/api/v1/user/phone_verify/request/", format="json", data=self.request_args_empty)
        self.assertEqual(response.status_code, 204) # No Content

        # Full request args
        response = self.api_client.post(
            "/api/v1/user/phone_verify/request/", format="json", data=self.request_args)
        authy_api.phones.verification_start.assert_called_with(**self.request_args)
        self.assertEqual(response.status_code, 200)

    @patch('new_dawn_server.users.api.resources.authy_api')
    def test_phone_verify_authenticate(self, authy_api):
        authy_api.phones.verification_check = MagicMock()
        request_sms_response = MagicMock()

        # Successful authentication
        request_sms_response.ok.return_value = True
        authy_api.phones.verification_check.return_value = request_sms_response
        response = self.api_client.post(
            '/api/v1/user/phone_verify/authenticate/', format="json", data=self.authenticate_args)
        authy_api.phones.verification_check.assert_called_with(**self.authenticate_args)
        self.assertEqual(response.status_code, 200)
        response["success"] = True

        # Failed authentication
        request_sms_response.ok.return_value = False
        authy_api.phones.verification_check.return_value = request_sms_response
        response = self.api_client.post(
            '/api/v1/user/phone_verify/authenticate/', format="json", data=self.authenticate_args)
        authy_api.phones.verification_check.assert_called_with(**self.authenticate_args)
        self.assertEqual(response.status_code, 406) # Not Acceptable
        response["success"] = False

