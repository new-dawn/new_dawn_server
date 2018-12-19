import json

from django.test import TestCase
from new_dawn_server.locations.college_constants import college_names
from tastypie.test import ResourceTestCaseMixin


class CollegeNameTest(ResourceTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()

    def test_get_collge_names(self):
        res = self.api_client.get(
            "/api/v1/city_preference/get_college_list/", format="json"
        )
        res_data = json.loads(res.content)
        self.assertEqual(res_data['college_list'], college_names)
