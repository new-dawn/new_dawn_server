from django.contrib.auth.models import User
from django.test import TestCase
from new_dawn_server.locations.models import CityPreference
from new_dawn_server.users.models import Account


class CityPreferenceTest(TestCase):
    def setUp(self):
        city1 = CityPreference.objects.create(
            city='New York',
            country='US',
            state='NY'
        )
        Account.objects.create(
            birthday="1996-01-01",
            gender="M",
            phone_number="+14004004400",
            name="testuser",
            user=User.objects.create()
        ).city_preference.add(city1)


    def test_city_preference(self):
        test_user = Account.objects.get(name="testuser")
        test_city_pref = test_user.city_preference.first()
        self.assertEqual(test_city_pref.city, "New York")
        self.assertEqual(test_city_pref.state, "NY")
        self.assertEqual(test_city_pref.country, "US")

    def test_user_has_multiple_preference(self):
        city2 = CityPreference.objects.create(
            city='Potomac',
            country='US',
            state='MD'
        )
        Account.objects.get(name="testuser").city_preference.add(city2)
        test_user = Account.objects.get(name="testuser")
        test_city_pref = test_user.city_preference.all()
        self.assertEqual(len(test_city_pref), 2)
        self.assertEqual(test_city_pref[1].city, "Potomac")
        self.assertEqual(test_city_pref[1].state, "MD")
        self.assertEqual(test_city_pref[1].country, "US")
