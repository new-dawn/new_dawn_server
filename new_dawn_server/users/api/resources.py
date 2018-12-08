from django import forms
from django.conf.urls import url
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import signals
import logging
from new_dawn_server.users.models import Account
from new_dawn_server.users.models import Profile
from new_dawn_server.questions.models import AnswerQuestion, Question
from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest
from tastypie.http import HttpUnauthorized, HttpForbidden
from tastypie.models import create_api_key
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS
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
        allowed_methods = ["get", "post"]
        authentication = Authentication()
        authorization = Authorization()
        excludes = ["is_staff", "password"]
        queryset = User.objects.all()
        resource_name = "user"

    def prepend_urls(self):
        # Override user/login and user/logout urls with login/logout views
        return [
            url(r"^user/login/$", self.wrap_view("login"), name="api_login"),
            url(r"^user/logout/$", self.wrap_view("logout"), name="api_logout"),
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
                    "reason": "disabled",
                }, HttpForbidden)
        else:
            return self.create_response(request, {
                "success": False,
                "reason": "incorrect",
            }, HttpUnauthorized)

    def logout(self, request, **kwargs):
        self.method_check(request, allowed=["get"])
        if request.user and request.user.is_authenticated():
            logout(request)
            return self.create_response(request, {"success": True})
        else:
            return self.create_response(request, {"success": False}, HttpUnauthorized)


class AccountResource(ModelResource):
    user = fields.ToOneField(UserResource, "user", related_name="account", full=True)

    class Meta:
        allowed_methods = ["get"]
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

    def dehydrate(self, bundle):
        # Add extra fields to the response
        bundle.data["username"] = bundle.obj.username
        bundle.data["token"] = bundle.obj.api_key.key
        return bundle
