import json

from django.test import TestCase
from new_dawn_server.locations.constants import us_city_mapping, country_list
from tastypie.test import ResourceTestCaseMixin


class CityMappingTest(ResourceTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.headers = {"Content-Type": "application/json"}
        self.country_testcase = {"country": "United States"}
        self.state_testcase = {"state": "Utah"}

    def test_get_country_list(self):
        res = self.api_client.get(
            "/api/v1/city_preference/get_country_list/", format="json"
        )
        res_data = json.loads(res.content)
        self.assertEqual(res_data['country_list'], ["United States"])

    def test_get_state_for_country(self):
        res = self.api_client.get(
            "/api/v1/city_preference/get_state_for_country/", data=self.country_testcase, headers=self.headers
        )
        res_data = json.loads(res.content)
        print(res_data)
        self.assertEqual(res_data["state_list"], country_list["United States"])
