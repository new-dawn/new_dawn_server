from django.test import TestCase
from django.contrib.auth.models import User
from new_dawn_server.actions.constants import ActionType, EntityType
from new_dawn_server.actions.models import UserAction
from new_dawn_server.users.models import Account


class LikeTest(TestCase):
    def setUp(self):
        from_user = Account.objects.create(
            birthday="1996-01-01",
            gender="M",
            phone_number="+14004004400",
            name="testuser_m",
            user=User.objects.create(username='ljl')
        )
        to_user = Account.objects.create(
            birthday="1995-01-01",
            gender="F",
            phone_number="+100000000",
            name="testuser_f",
            user=User.objects.create(username='nn')
        )
        UserAction.objects.create(
            action_type=ActionType.LIKE.value,
            entity_id=1,
            entity_type=EntityType.MAIN_IMAGE.value,
            user_account_from=from_user,
            user_account_to=to_user,
        )

    def test_get_user_likes(self):
        test_account = Account.objects.get(name="testuser_m")
        test_like_obj = UserAction.objects.get(user_account_from=test_account)
        self.assertEqual(test_like_obj.user_account_to.name, "testuser_f")
        self.assertEqual(test_like_obj.action_type, ActionType.LIKE.value)
        self.assertEqual(test_like_obj.entity_id, 1)
        self.assertEqual(test_like_obj.entity_type, EntityType.MAIN_IMAGE.value)

    def test_get_multiple_user_likes(self):
        Account.objects.create(
            birthday="1995-01-01",
            gender="F",
            phone_number="+100000000",
            name="awa",
            user=User.objects.create(username='ww')
        )
        UserAction.objects.create(
            action_type=ActionType.LIKE.value,
            user_account_from=Account.objects.get(name="testuser_m"),
            user_account_to=Account.objects.get(name="awa"),
            entity_type=EntityType.QUESTION_ANSWER.value,
            entity_id=1
        )
        test_like_objs = UserAction.objects.filter(user_account_from__name="testuser_m")
        self.assertEqual(test_like_objs[0].user_account_to.name, "testuser_f")
        self.assertEqual(test_like_objs[0].entity_id, 1)
        self.assertEqual(test_like_objs[0].entity_type, EntityType.MAIN_IMAGE.value)
        self.assertEqual(test_like_objs[0].action_type, ActionType.LIKE.value)
        self.assertEqual(test_like_objs[1].user_account_to.name, "awa")
        self.assertEqual(test_like_objs[1].entity_id, 1)
        self.assertEqual(test_like_objs[1].entity_type, EntityType.QUESTION_ANSWER.value)
        self.assertEqual(test_like_objs[1].action_type, ActionType.LIKE.value)
