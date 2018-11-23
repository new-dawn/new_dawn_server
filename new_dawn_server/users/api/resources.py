from django import forms
from django.contrib.auth.models import User
from django.db import IntegrityError
from new_dawn_server.users.models import Account
from new_dawn_server.users.models import Profile
from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest
from tastypie.resources import ModelResource
from tastypie.validation import Validation

# Fields of each model
# The bool value means required if True
USER_FIELDS = {
	'username': True,
	'password': True,
	'first_name': True,
	'last_name': True,
}

ACCOUNT_FIELDS = {
	'birthday': True,
}

PROFILE_FIELDS = {
	
}


class UserResource(ModelResource):
	
	class Meta:
		allowed_methods = ['get']
		authentication = Authentication()
		authorization = Authorization()
		excludes = ['is_staff', 'password']
		queryset = User.objects.all()
		resource_name = 'user'


class AccountResource(ModelResource):
	user = fields.ToOneField(UserResource, 'user', related_name='account', full=True)

	class Meta:
		allowed_methods = ['get']
		authentication = Authentication()
		authorization = Authorization()
		queryset = Account.objects.all()
		resource_name = 'account'


class ProfileResource(ModelResource):
	user = fields.ToOneField(UserResource, 'user', related_name='profile', full=True)

	class Meta:
		allowed_methods = ['get']
		authentication = Authentication()
		authorization = Authorization()
		queryset = Profile.objects.all()
		resource_name = 'profile'


class UserRegisterValidation(Validation):
    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {'__all__': 'No data found in the bundle'}
        not_found_fields = {}
        for field, required in {**USER_FIELDS, **ACCOUNT_FIELDS, **PROFILE_FIELDS}.items():
        	if required and field not in bundle.data:
        		not_found_fields[field] = 'Required field not found'
        return not_found_fields


class UserRegisterResource(ModelResource):
	class Meta:
		allowed_methods = ['post']
		authentication = Authentication()
		authorization = Authorization()
		include_resource_uri = False
		queryset = User.objects.all()
		resource_name = 'register'
		validation = UserRegisterValidation()

	def obj_create(self, bundle, **kwargs):
		try:
			user_bundle = super(UserRegisterResource, self).obj_create(bundle, **kwargs)
			user_bundle.obj.set_password(bundle.data.get('password'))
			user_bundle.obj.save()
			account = Account(
				birthday=bundle.data.get("birthday"),
				user=user_bundle.obj,
			)
			account.save()
			profile = Profile(
				account=account,
				user=user_bundle.obj,
			)
			profile.save()
		except IntegrityError:
			raise BadRequest('Username already exists')
		return bundle




