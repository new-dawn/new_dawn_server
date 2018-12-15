from authy.api import AuthyApiClient
from django import forms
from django.conf import settings
from django.conf.urls import url
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import signals
from new_dawn_server.locations.api.resources import CityResource
from new_dawn_server.locations.models import CityPreference
from new_dawn_server.questions.models import AnswerQuestion
from new_dawn_server.users.models import Account
from new_dawn_server.users.models import Profile
from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest
from tastypie.http import HttpForbidden, HttpNotAcceptable, HttpNoContent, HttpUnauthorized
from tastypie.models import create_api_key
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS, ALL
from tastypie.utils import trailing_slash
from tastypie.validation import Validation

# Create an API key whenever a User is created
# This API key will be stored in front-end and be used
# to access private views
signals.post_save.connect(create_api_key, sender=User)

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

# Create authentication client
authy_api = AuthyApiClient(settings.ACCOUNT_SECURITY_API_KEY)


class UserResource(ModelResource):
    class Meta:
        allowed_methods = ["get", "post"]
        authentication = Authentication()
        authorization = Authorization()
        excludes = ["is_staff", "password"]
        filtering = {"username": "exact"}
        queryset = User.objects.all()
        resource_name = "user"

    def prepend_urls(self):
        # Override user/login and user/logout urls with login/logout views
        return [
            url(r"^user/login/$", self.wrap_view("login"), name="api_login"),
            url(r"^user/logout/$", self.wrap_view("logout"), name="api_logout"),
            url(r"^user/phone_verify/request/$",
                self.wrap_view("phone_verify_request"), name="api_phone_verify_request"),
            url(r"^user/phone_verify/authenticate/$",
                self.wrap_view("phone_verify_authenticate"), name="api_phone_verify_authenticate"),
        ]

    def login(self, request, **kwargs):
        self.method_check(request, allowed=["post"])

        data = self.deserialize(request, request.body, format=request.META.get("CONTENT_TYPE", "application/json"))

        username = data.get("username", "")
        password = data.get("password", "")

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                # Return username and access token to store in iOS keychain
                return self.create_response(request, {
                    "success": True,
                    "username": user.username,
                    "token": user.api_key.key,
                })
            else:
                return self.create_response(request, {
                    "success": False,
                    "message": "disabled",
                }, HttpForbidden)
        else:
            return self.create_response(request, {
                "success": False,
                "message": "incorrect",
            }, HttpUnauthorized)

    def logout(self, request, **kwargs):
        self.method_check(request, allowed=["get"])
        if request.user and request.user.is_authenticated():
            logout(request)
            return self.create_response(request, {"success": True})
        else:
            return self.create_response(request, {"success": False}, HttpUnauthorized)

    def phone_verify_request(self, request, **kwargs):
        self.method_check(request, allowed=["post"])
        data = self.deserialize(request, request.body, format=request.META.get("CONTENT_TYPE", "application/json"))
        phone_number = data.get("phone_number", "")
        country_code = data.get("country_code", "")
        via = data.get("via", "sms")
        if phone_number and country_code:
            # Start sending verification code
            authy_api.phones.verification_start(
                phone_number=phone_number,
                country_code=country_code,
                via=via
            )
            return self.create_response(request, {"success": True, "message": "Verification Code Sent"})
        else:
            return self.create_response(
                request, {"success": False, "message": "Missing phone_number or country_code"}, HttpNoContent)

    def phone_verify_authenticate(self, request, **kwargs):
        self.method_check(request, allowed=["post"])
        data = self.deserialize(request, request.body, format=request.META.get("CONTENT_TYPE", "application/json"))
        phone_number = data.get("phone_number", "")
        country_code = data.get("country_code", "")
        verification_code = data.get("verification_code", "")
        if phone_number and country_code:
            verification = authy_api.phones.verification_check(
                phone_number=phone_number,
                country_code=country_code,
                verification_code=verification_code
            )
            if verification.ok():
                return self.create_response(request, {"success": True, "message": "Verification Successful"})
            else:
                error_msg = ":".join([err for err in verification.errors().values()])
                return self.create_response(
                    request, {"success": False, "message": error_msg}, HttpNotAcceptable)
        else:
            return self.create_response(
                request, {"success": False, "message": "Missing phone_number or country_code"}, HttpNoContent)


class AccountResource(ModelResource):
    user = fields.ToOneField(UserResource, "user", related_name="account", full=True)
    city_preference = fields.ManyToManyField(CityResource, "city_preference", related_name="account", full=True)

    class Meta:
        allowed_methods = ["get"]
        always_return_data = True
        authentication = Authentication()
        authorization = Authorization()
        queryset = Account.objects.all()
        resource_name = "account"


class ProfileResource(ModelResource):
    account = fields.ToOneField(AccountResource, "account", related_name="profile", full=True)
    user = fields.ToOneField(UserResource, "user", related_name="profile", full=True)

    class Meta:
        allowed_methods = ["get"]
        authentication = Authentication()
        authorization = Authorization()
        filtering = {
            'user': ALL_WITH_RELATIONS
        }
        queryset = Profile.objects.all()
        resource_name = "profile"

    @staticmethod
    def _get_all_questions_answers(answer_question_obj):
        result_list = []
        for answer_question in answer_question_obj:
            one_question_answer_dict = {
                'question': answer_question.question.question,
                'answer': answer_question.answer,
                'order': answer_question.order,
                "update_time": answer_question.update_time,
            }
            result_list.append(one_question_answer_dict)
        return result_list

    # Add Answer question fields in Profile Resource
    def dehydrate(self, bundle):
        user_id = bundle.data['user'].data['id']
        answer_question_obj = AnswerQuestion.objects.filter(user_id=user_id)
        answer_question_lists = self._get_all_questions_answers(answer_question_obj)
        bundle.data['answer_question'] = answer_question_lists
        return bundle


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
        always_return_data = True
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

    @staticmethod
    def deserialize_city_pref(bundle, account):
        pref_city_list = bundle.data.get("city_preference")
        if pref_city_list:
            for location in pref_city_list:
                city_pref = CityPreference(
                    city=location['city'],
                    state=location['state'],
                    country=location['country']
                )
                city_pref.save()
                account.city_preference.add(city_pref)

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

            # Deserialize City Preference Information and add to account
            self.deserialize_city_pref(bundle, account)

            profile = Profile(
                user=user_bundle.obj,
                account=account,
                **self._get_model_fields_dict(bundle, PROFILE_FIELDS)
            )
            profile.save()
        return bundle

    def dehydrate(self, bundle):
        # Add extra fields to the response
        bundle.data["username"] = bundle.obj.username
        bundle.data["token"] = bundle.obj.api_key.key
        return bundle
