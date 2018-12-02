from django import forms
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db import transaction
from new_dawn_server.users.models import Account
from new_dawn_server.users.models import Profile
from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest
from tastypie.resources import ModelResource
from tastypie.validation import Validation

# Fields of each user-related model
# The bool value means if the field is required 
# during INITIAL registration

USER_FIELDS = {
	"username": True,
	"password": True,
	"first_name": True,
	"last_name": True,
}

ACCOUNT_FIELDS = {
	"birthday": False,
	"gender": False,
	"phone_number": False,
}

PROFILE_FIELDS = {
	"city_preference": False,
	"description": False,
	"employer": False,
	"height": False,
	"hometown": False,
	"job_title": False,
	"profile_photo_url": False,
	"school": False,
	"smoke": False,
}

# Account Name Delimiter
ACCOUNT_NAME_DELIMITER = "_"


class UserResource(ModelResource):
	
	class Meta:
		allowed_methods = ["get"]
		authentication = Authentication()
		authorization = Authorization()
		excludes = ["is_staff", "password"]
		queryset = User.objects.all()
		resource_name = "user"


class AccountResource(ModelResource):
	user = fields.ToOneField(UserResource, "user", related_name="account", full=True)

	class Meta:
		allowed_methods = ["get"]
		authentication = Authentication()
		authorization = Authorization()
		queryset = Account.objects.all()
		resource_name = "account"


class ProfileResource(ModelResource):
	account = fields.ToOneField(UserResource, "account", related_name="profile", full=True)
	user = fields.ToOneField(UserResource, "user", related_name="profile", full=True)

	class Meta:
		allowed_methods = ["get"]
		authentication = Authentication()
		authorization = Authorization()
		queryset = Profile.objects.all()
		resource_name = "profile"


class UserRegisterValidation(Validation):
    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {"__all__": "No data found in the bundle"}
        not_found_fields = {}
        for field, required in {**USER_FIELDS, **ACCOUNT_FIELDS, **PROFILE_FIELDS}.items():
        	if required and field not in bundle.data:
        		not_found_fields[field] = "Required field not found"
        return not_found_fields


class UserRegisterResource(ModelResource):
	class Meta:
		allowed_methods = ["post"]
		authentication = Authentication()
		authorization = Authorization()
		include_resource_uri = False
		queryset = User.objects.all()
		resource_name = "register"
		validation = UserRegisterValidation()

	@staticmethod
	def _get_model_fields_dict(bundle, fields):
		result_dict = {}
		for field, _ in fields.items():
			# The field can be None if it's not in the bundle
			result_dict[field] = bundle.data.get(field)
		return result_dict

	@staticmethod
	def _get_account_name(first_name, last_name):
		return first_name + ACCOUNT_NAME_DELIMITER + last_name

	def obj_create(self, bundle, **kwargs):
		"""
		Override obj_create method to create related models
		"""
		# Either all models are successfully created or no model is created
		# TODO: Catch exception with Django Logging
		with transaction.atomic():
			user_bundle = super(UserRegisterResource, self).obj_create(bundle, **kwargs)
			user_bundle.obj.set_password(bundle.data.get("password"))
			user_bundle.obj.save()
			account = Account(
				user=user_bundle.obj,
				name=self._get_account_name(user_bundle.obj.first_name, user_bundle.obj.last_name),
				**self._get_model_fields_dict(bundle, ACCOUNT_FIELDS)
			)
			account.save()
			profile = Profile(
				user=user_bundle.obj,
				account=account,
				**self._get_model_fields_dict(bundle, PROFILE_FIELDS)
			)
			profile.save()
		return bundle
