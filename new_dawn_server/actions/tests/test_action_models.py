from django.test import TestCase
from django.contrib.auth.models import User
from new_dawn_server.actions.constants import ActionType, EntityType
from new_dawn_server.actions.models import UserAction


class LikeTest(TestCase):
    def setUp(self):
        from_user = User.objects.create(username='ljl')

        to_user = User.objects.create(username='nn')

        UserAction.objects.create(
            action_type=ActionType.LIKE.value,
            entity_id=1,
            entity_type=EntityType.MAIN_IMAGE.value,
            user_from=from_user,
            user_to=to_user,
        )

    def test_get_user_likes(self):
        test_user = User.objects.get(username="ljl")
        test_like_obj = UserAction.objects.get(user_from=test_user)
        self.assertEqual(test_like_obj.user_to.username, "nn")
        self.assertEqual(test_like_obj.action_type, ActionType.LIKE.value)
        self.assertEqual(test_like_obj.entity_id, 1)
        self.assertEqual(test_like_obj.entity_type, EntityType.MAIN_IMAGE.value)

    def test_get_multiple_user_likes(self):
        User.objects.create(username="gg")
        UserAction.objects.create(
            action_type=ActionType.LIKE.value,
            user_from=User.objects.get(username="ljl"),
            user_to=User.objects.get(username="gg"),
            entity_type=EntityType.QUESTION_ANSWER.value,
            entity_id=1
        )
        test_like_objs = UserAction.objects.filter(user_from__username="ljl")
        self.assertEqual(test_like_objs[0].user_to.username, "nn")
        self.assertEqual(test_like_objs[0].entity_id, 1)
        self.assertEqual(test_like_objs[0].entity_type, EntityType.MAIN_IMAGE.value)
        self.assertEqual(test_like_objs[0].action_type, ActionType.LIKE.value)
        self.assertEqual(test_like_objs[1].user_to.username, "gg")
        self.assertEqual(test_like_objs[1].entity_id, 1)
        self.assertEqual(test_like_objs[1].entity_type, EntityType.QUESTION_ANSWER.value)
        self.assertEqual(test_like_objs[1].action_type, ActionType.LIKE.value)
