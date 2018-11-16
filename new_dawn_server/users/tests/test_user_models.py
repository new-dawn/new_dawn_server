import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from new_dawn_server.users.models import Account

class AccountTest(TestCase):
	def setUp(self):
		Account.objects.create(
			birthday="1996-01-01", 
			gender="M", 
			phone_number="+14004004400",
			name="testuser",
			user=User.objects.create()
		)

	def test_account_basic_info(self):
		test_user = Account.objects.get(name="testuser")
		self.assertEqual(test_user.name, "testuser")
		self.assertEqual(test_user.gender, "M")
		self.assertEqual(test_user.get_gender_display(), "Male")
		self.assertEqual(test_user.birthday, datetime.date(1996, 1, 1))
	
	def test_account_phone_number(self):
		test_user = Account.objects.get(name="testuser")
		self.assertEqual(test_user.phone_number.as_international, "+1 400-400-4400")
		# TODO (ljl): Add more assertEqual to different form of output we can get

# TODO (ljl): Add unit test for Profile model