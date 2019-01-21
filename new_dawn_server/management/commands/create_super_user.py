import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

class Command(BaseCommand):

	def handle(self, *args, **options):
		if 'SUPER_USER_NAME' in os.environ and 'SUPER_USER_EMAIL' in os.environ and 'SUPER_USER_PASSWORD' in os.environ:
			username = os.environ['SUPER_USER_NAME']
			if not User.objects.filter(username=username).exists():
				User.objects.create_superuser(
					username, os.environ['SUPER_USER_EMAIL'], os.environ['SUPER_USER_PASSWORD'])
			admin_user = User.objects.get(username=username)
			print("Super User Created: " + admin_user.username)
			print("Api-Key: " + admin_user.api_key.key)