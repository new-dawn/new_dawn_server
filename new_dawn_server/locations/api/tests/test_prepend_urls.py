import json

from django.test import TestCase
from new_dawn_server.locations.constants.city_constants import us_city_mapping, country_list
from tastypie.test import ResourceTestCaseMixin


class CityMappingTest(ResourceTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
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
            "/api/v1/city_preference/get_state_for_country/", format='json', data=self.country_testcase
        )
        res_data = json.loads(res.content)
        self.assertEqual(res_data["state_list"], country_list["United States"])

    def test_get_city_for_state(self):
        city_state_testcase = {**self.country_testcase, **self.state_testcase}
        res = self.api_client.get(
            "/api/v1/city_preference/get_city_for_state/", format='json', data=city_state_testcase
        )
        res_data = json.loads(res.content)
        self.assertEqual(res_data["city_list"], us_city_mapping["Utah"])