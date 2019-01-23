from django.test import TestCase
from django.contrib.auth.models import User
from new_dawn_server.actions.constants import EntityType
from new_dawn_server.actions.models import Like, UserToUserActionMetadata
from new_dawn_server.users.models import Account


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

        test_meta = UserToUserActionMetadata.objects.create(
            user_account_from=Account.objects.get(name="testuser_m"),
            user_account_to=Account.objects.get(name="testuser_f"),
            entity_type=EntityType.MAIN_IMAGE.value,
            entity_id=1
        )
        Like.objects.create(like_metadata=test_meta)

    def test_get_user_likes(self):
        test_like_obj = Like.objects.get(like_metadata__user_account_from__name="testuser_m")
        self.assertEqual(test_like_obj.like_metadata.user_account_to.name, "testuser_f")
        self.assertEqual(test_like_obj.like_metadata.entity_id, 1)
        self.assertEqual(test_like_obj.like_metadata.entity_type, EntityType.MAIN_IMAGE.value)

    def test_get_multiple_user_likes(self):
        Account.objects.create(
            birthday="1995-01-01",
            gender="F",
            phone_number="+100000000",
            name="awa",
            user=User.objects.create(username='ww')
        )
        Like.objects.create(like_metadata=UserToUserActionMetadata.objects.create(
            user_account_from=Account.objects.get(name="testuser_m"),
            user_account_to=Account.objects.get(name="awa"),
            entity_type=EntityType.QUESTION_ANSWER.value,
            entity_id=1
        ))
        test_like_objs = Like.objects.filter(like_metadata__user_account_from__name="testuser_m")
        self.assertEqual(test_like_objs[0].like_metadata.user_account_to.name, "testuser_f")
        self.assertEqual(test_like_objs[0].like_metadata.entity_id, 1)
        self.assertEqual(test_like_objs[0].like_metadata.entity_type, EntityType.MAIN_IMAGE.value)
        self.assertEqual(test_like_objs[1].like_metadata.user_account_to.name, "awa")
        self.assertEqual(test_like_objs[1].like_metadata.entity_id, 1)
        self.assertEqual(test_like_objs[1].like_metadata.entity_type, EntityType.QUESTION_ANSWER.value)
