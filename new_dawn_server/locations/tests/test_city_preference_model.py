from django.contrib.auth.models import User
from django.test import TestCase
from new_dawn_server.locations.models import CityPreference
from new_dawn_server.users.models import Account


class CityPreferenceTest(TestCase):
    def setUp(self):
        self.city1 = CityPreference.objects.create(
            city='New York',
            country='US',
            state='NY'
        )

        self.city2 = CityPreference.objects.create(
            city='Potomac',
            country='US',
            state='MD'
        )

        self.account1 = Account.objects.create(
            birthday="1996-01-01",
            gender="M",
            phone_number="+14004004400",
            name="testuser",
            user=User.objects.create(username="aa", password="aa")
        )
        # Multiple City Preference
        self.account1.city_preference.add(self.city1)
        self.account1.city_preference.add(self.city2)

        self.account2 = Account.objects.create(
            birthday="1996-02-02",
            gender="F",
            phone_number="+14004004400",
            name="testuser2",
            user=User.objects.create(username="bb", password="bb")
        )
        self.account2.city_preference.add(self.city1)


    def test_city_preference(self):
        test_user = Account.objects.get(name="testuser")
        test_city_pref = test_user.city_preference.first()
        self.assertEqual(test_city_pref.city, "New York")
        self.assertEqual(test_city_pref.state, "NY")
        self.assertEqual(test_city_pref.country, "US")

    def test_user_has_multiple_preference(self):
        test_user = Account.objects.get(name="testuser")
        test_city_pref = test_user.city_preference.all()
        self.assertEqual(len(test_city_pref), 2)
        self.assertEqual(test_city_pref[1].city, "Potomac")
        self.assertEqual(test_city_pref[1].state, "MD")
        self.assertEqual(test_city_pref[1].country, "US")

    def test_preference_has_multiple_user(self):
        # Reverse relationship
        test_city_pref = CityPreference.objects.filter(city="New York")[0]
        test_users = test_city_pref.account_set.all()
        self.assertEqual(test_users[0].name, self.account1.name)
        self.assertEqual(test_users[1].name, self.account2.name)

