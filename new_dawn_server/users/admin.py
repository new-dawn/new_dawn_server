from django.contrib import admin
from new_dawn_server.users.models import Account
from new_dawn_server.users.models import Profile

admin.site.register(Account)
admin.site.register(Profile)
