from django.contrib.auth.models import User
from django.test import TestCase
from new_dawn_server.locations.models import CityPreference, Country, State
from new_dawn_server.users.models import Account


class CityPreferenceTest(TestCase):
    def setUp(self):
        CityPreference.objects.create(
            city="New York",
            state=State.objects.create(
                country=Country.objects.create(country="US"),
                state="NY"
            ),
            user_account=Account.objects.create(
                birthday="1996-01-01",
                gender="M",
                phone_number="+14004004400",
                name="testuser",
                user=User.objects.create(),
            )
        )

    def test_city_preference(self):
        test_user = Account.objects.get(name="testuser")
        test_city_pref = CityPreference.objects.get(user_account=test_user)
        self.assertEqual(test_city_pref.city, "New York")
        self.assertEqual(test_city_pref.state.state, "NY")
        self.assertEqual(test_city_pref.state.country.country, "US")

    def test_user_has_multiple_preference(self):
        CityPreference.objects.create(
            city="Potomac",
            state=State.objects.create(
                country=Country.objects.create(country="US"),
                state="MD"
            ),
            user_account=Account.objects.get(name="testuser")
        )
        test_user = Account.objects.get(name="testuser")
        test_city_pref = CityPreference.objects.filter(user_account=test_user)
        self.assertEqual(len(test_city_pref), 2)
        self.assertEqual(test_city_pref[1].city, "Potomac")
        self.assertEqual(test_city_pref[1].state.state, "MD")
        self.assertEqual(test_city_pref[1].state.country.country, "US")
