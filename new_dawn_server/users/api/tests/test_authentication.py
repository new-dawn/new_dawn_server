import json

from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin


# MultiAuthentication works when any of its authentication method is fulfilled
class AuthenticationTest(ResourceTestCaseMixin, TestCase):
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
        res_data = json.loads(res.content)
        self.api_credential = self.create_apikey(username=res_data["username"], api_key=res_data["token"])
        self.basic_credential = self.create_basic(username=res_data["username"],
                                                  password=self.register_arguments["password"])

    def test_basic_authentication(self):
        res = self.api_client.get("/api/v1/profile/", format="json")
        self.assertEquals(res.status_code, 401)

        res = self.api_client.get("/api/v1/profile/", format="json", authentication=self.basic_credential)
        self.assertEquals(res.status_code, 200)

    def test_api_authenticatoin(self):
        res = self.api_client.get("/api/v1/profile/", format="json")
        self.assertEquals(res.status_code, 401)

        res = self.api_client.get("/api/v1/profile/", format="json", authentication=self.api_credential)
        self.assertEquals(res.status_code, 200)
