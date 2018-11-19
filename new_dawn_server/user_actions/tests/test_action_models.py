from django.test import TestCase
from django.contrib.auth.models import User
from new_dawn_server.users.models import Account, Profile
from new_dawn_server.user_actions.models import Block, Grade, Like, Relationship

from decimal import Decimal


class LikeTest(TestCase):
    def setUp(self):
        Account.objects.create(
            birthday="1996-01-01",
            gender="M",
            phone_number="+14004004400",
            name="testuser_m",
            user=User.objects.create(username='ljl')
        )
        Profile.objects.create(
            account=Account.objects.get(name="testuser_m"),
            city_preference="New York",
            description="Good Boy",
            employer="ManMan",
            height=Decimal(180.00),
            hometown="Chongqing",
            job_title="Analyst",
            school="NYU",
            smoke="True"
        )
        Account.objects.create(
            birthday="1995-01-01",
            gender="F",
            phone_number="+100000000",
            name="testuser_f",
            user=User.objects.create(username='nn')
        )
        Profile.objects.create(
            account=Account.objects.get(name="testuser_f"),
            city_preference="New York",
            description="Good Boy",
            employer="ManMan",
            height=Decimal(180.00),
            hometown="Chongqing",
            job_title="Analyst",
            school="NYU",
            smoke="True"
        )
        Like.objects.create(
            user_profile_like=Profile.objects.get(account=Account.objects.get(name='testuser_f')),
            user_profile_liked=Profile.objects.get(account=Account.objects.get(name='testuser_m')),
            match=False
        )

        Block.objects.create(
            user_account_block=Account.objects.get(name='testuser_f'),
            user_account_blocked=Account.objects.get(name='testuser_m'),
        )
        Grade.objects.create(
            user_account_given=Account.objects.get(name='testuser_f'),
            user_account_received=Account.objects.get(name='testuser_m'),
            grade=5,
        )
        Relationship.objects.create(
            user_account_relationship_invite=Account.objects.get(name='testuser_f'),
            user_account_relationship_receive=Account.objects.get(name='testuser_m'),
            in_relationship=True
        )

    def test_user_actions_block(self):
        test_user_account = Account.objects.get(name="testuser_f")
        test_user_block = Block.objects.get(user_account_block=test_user_account)
        self.assertEqual(test_user_block.user_account_blocked.name, "testuser_m")

    def test_user_actions_grade(self):
        test_user_account = Account.objects.get(name="testuser_f")
        test_user_grade = Grade.objects.get(user_account_given=test_user_account)
        self.assertEqual(test_user_grade.user_account_received.name, "testuser_m")
        self.assertEqual(test_user_grade.grade, 5)

    def test_user_actions_like(self):
        test_user_account = Account.objects.get(name="testuser_m")
        test_user_profile = Profile.objects.get(account=test_user_account)
        test_user_like = Like.objects.get(user_profile_liked=test_user_profile)
        self.assertEqual(test_user_like.user_profile_like.account.name, "testuser_f")
        self.assertEqual(test_user_like.user_profile_liked.account.name, "testuser_m")

    def test_user_actions_relationship(self):
        test_user_account = Account.objects.get(name="testuser_f")
        test_user_relation = Relationship.objects.get(user_account_relationship_invite=test_user_account)
        self.assertEqual(test_user_relation.in_relationship, True)
        self.assertEqual(test_user_relation.user_account_relationship_receive.name, "testuser_m")
