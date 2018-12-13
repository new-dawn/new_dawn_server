import json

from django.test import TestCase
from new_dawn_server.locations.models import CityPreference
from tastypie.test import ResourceTestCaseMixin


class CityPreferenceTest(ResourceTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.city_preference_arguments = {
            "city": "New York",
            "state": "NY",
            "country": "US"
        }

    def test_location_post(self):
        self.assertEqual(CityPreference.objects.count(), 0)
        res = self.api_client.post("/api/v1/city_preference/", format="json", data=self.city_preference_arguments)
        res_data = json.loads(res.content)
        self.assertEqual(CityPreference.objects.count(), 1)
        for k, v in self.city_preference_arguments.items():
            self.assertEqual(res_data[k], v)
