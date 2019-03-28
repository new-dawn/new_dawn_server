import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from new_dawn_server.actions.constants import ActionType, EntityType
from new_dawn_server.actions.models import UserAction

class Command(BaseCommand):


    def create_like_image(self, a, b):
        # Create Match
        print(f"Like from {a} to {b}")
        UserAction.objects.create(
            action_type = ActionType.LIKE.value,
            entity_id = 1,
            entity_type = EntityType.MAIN_IMAGE.value,
            user_from = User.objects.get(id=a),
            user_to = User.objects.get(id=b),
            message = "This looks great!"
        )

    def create_like_answer(self, a, b):
        # Create Match
        print(f"Like from {a} to {b}")
        UserAction.objects.create(
            action_type = ActionType.LIKE.value,
            entity_id = 1,
            entity_type = EntityType.QUESTION_ANSWER.value,
            user_from = User.objects.get(id=a),
            user_to = User.objects.get(id=b),
            message = "Sounds legit!"
        )

    def create_match(self, a, b):
        # Create Match
        print(f"Relationship between {a} and {b}")
        UserAction.objects.create(
            action_type = ActionType.MATCH.value,
            entity_id = 0,
            entity_type = EntityType.NONE.value,
            user_from = User.objects.get(id=a),
            user_to = User.objects.get(id=b)
        )

    def create_message(self, a, b, message):
        # Create Message
        print(f"Message between {a} and {b}")
        UserAction.objects.create(
            action_type = ActionType.MESSAGE.value,
            entity_id = 0,
            entity_type = EntityType.NONE.value,
            user_from = User.objects.get(id=a),
            user_to = User.objects.get(id=b),
            message = message
        )

    def handle(self, *args, **options):
        print("Create User Actions")
        self.create_like_image(4,1)
        self.create_like_answer(3,1)
        self.create_match(1,2)
        self.create_match(1,3)
        self.create_message(1,2,"Hey there!")
        self.create_message(2,1,"Hey what's up.")
        self.create_message(1,3,"Hello I like you!")
        self.create_message(1,3,"Can you talk to me?")
        self.create_message(3,1,"Sure why not")