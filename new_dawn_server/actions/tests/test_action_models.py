from django.test import TestCase
from django.contrib.auth.models import User
from new_dawn_server.users.models import Account
from new_dawn_server.actions.models import ActionsMetadata



class LikeTest(TestCase):
    def setUp(self):
        Account.objects.create(
            birthday="1996-01-01",
            gender="M",
            phone_number="+14004004400",
            name="testuser_m",
            user=User.objects.create(username='ljl')
        )
        Account.objects.create(
            birthday="1995-01-01",
            gender="F",
            phone_number="+100000000",
            name="testuser_f",
            user=User.objects.create(username='nn')
        )
        ActionsMetadata.objects.create(
            user_account_from=Account.objects.get(name="testuser_m"),
            user_account_to=Account.objects.get(name="testuser_f")
        )

