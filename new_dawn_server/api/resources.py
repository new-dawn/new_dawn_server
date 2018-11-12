from django.contrib.auth.models import User
from new_dawn_server.users.models import Account
from tastypie.resources import ModelResource
from tastypie import fields

class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		resource_name = 'user'

class AccountResource(ModelResource):
	user = fields.ForeignKey(UserResource, 'user')
	
	class Meta:
		queryset = Account.objects.all()
		allowed_methods = ['get']