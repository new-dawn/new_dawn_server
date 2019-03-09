import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from new_dawn_server.actions.constants import ActionType, EntityType
from new_dawn_server.actions.models import UserAction

class Command(BaseCommand):

    def create_relationship(self, a, b):
        # Create relationship
        print(f"Relationship between {a} and {b}")
        UserAction.objects.create(
            action_type = ActionType.RELATIONSHIP.value,
            entity_id = 0,
            entity_type = EntityType.NONE.value,
            user_from = User.objects.get(id=a),
            user_to = User.objects.get(id=b)
        )

    def create_message(self, a, b, message):
        # Create relationship
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
        self.create_relationship(1,2)
        self.create_relationship(1,3)
        self.create_message(1,2,"Hey there!")
        self.create_message(2,1,"Hey what's up.")
        self.create_message(1,3,"Hello I like you!")
        self.create_message(1,3,"Can you talk to me?")
        self.create_message(3,1,"Sure why not")