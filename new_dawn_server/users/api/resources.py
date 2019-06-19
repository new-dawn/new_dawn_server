from authy.api import AuthyApiClient
from datetime import date
import datetime
from django import forms
from django.conf import settings
from django.conf.urls import url
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from django.db.models import signals
from django.http import JsonResponse
from new_dawn_server.actions.constants import ActionType, EntityType
from new_dawn_server.actions.models import UserAction
from new_dawn_server.locations.api.resources import CityResource
from new_dawn_server.locations.models import CityPreference
from new_dawn_server.medias.models import Image
from new_dawn_server.modules.client_response import ClientResponse
from new_dawn_server.pusher.notification_service import NotificationService
from new_dawn_server.questions.models import AnswerQuestion, Question
from new_dawn_server.settings import MEDIA_URL
from new_dawn_server.users.models import Account
from new_dawn_server.users.models import Profile
from tastypie import fields
from tastypie.authentication import (
    ApiKeyAuthentication,
    Authentication,
    BasicAuthentication,
    MultiAuthentication
)
import os
from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest
from tastypie.http import HttpForbidden, HttpNotAcceptable, HttpNoContent, HttpUnauthorized
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
    "degree": False,
    "description": False,
    "drink": False,
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
        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()
        excludes = ["is_staff", "password"]
        filtering = {"username": "exact", "id": "exact"}
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
            url(r"^user/notification/authenticate/$",
                self.wrap_view("notification_authenticate"), name="api_notification_authenticate"),
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
                client_response_success = ClientResponse(
                    success=True,
                    message="Login Successful",
                    username=user.username,
                    token=user.api_key.key,
                )

                return self.create_response(
                    request, client_response_success.get_response_as_dict())
            else:
                return self.create_response(request, ClientResponse(
                    success=False,
                    message="Account has been disabled",
                ).get_response_as_dict(), HttpForbidden)
        else:
            return self.create_response(request, ClientResponse(
                success=False,
                message="Account login info doesn't match",
            ).get_response_as_dict(), HttpUnauthorized)

    def logout(self, request, **kwargs):
        self.method_check(request, allowed=["get"])
        if request.user and request.user.is_authenticated():
            logout(request)
            return self.create_response(request, ClientResponse(
                success=True,
                message="Logout Successful",
            ).get_response_as_dict())
        else:
            return self.create_response(request, ClientResponse(
                success=False,
                message="Logout Failed: Not authenticated",
            ).get_response_as_dict(), HttpUnauthorized)

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
            return self.create_response(request, ClientResponse(
                success=True,
                message="Verification Code Sent",
            ).get_response_as_dict())
        else:
            return self.create_response(
                request, ClientResponse(
                    success=False,
                    message="Missing country code and phone number",
                ).get_response_as_dict(), HttpNoContent)

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
                exist = False
                # Phone number by default is used as username
                user = User.objects.filter(username=phone_number)
                if user.count():
                    exist = True
                return self.create_response(request, ClientResponse(
                    success=True,
                    message="Verification Successful",
                    exist=exist,
                    user_id=user[0].id if user.count() else 0,
                    username=user[0].username if user.count() else "",
                    token=user[0].api_key.key if user.count() else "",
                ).get_response_as_dict())
            else:
                error_msg = ":".join([err for err in verification.errors().values()])
                return self.create_response(request, ClientResponse(
                    success=False,
                    message=error_msg,
                ).get_response_as_dict(), HttpNotAcceptable)
        else:
            return self.create_response(
                request, ClientResponse(
                    success=False,
                    message="Missing country code and phone number",
                ).get_response_as_dict(), HttpNoContent)

    def notification_authenticate(self, request, **kwargs):
        self.method_check(request, allowed=["get"])
        query_string = request.META["QUERY_STRING"]
        user_id = query_string.split("=")[1]
        if User.objects.filter(id=int(user_id)):
            beams_token = NotificationService().beams_auth(user_id)
            return JsonResponse(beams_token)
        else:
            return self.create_response(
                request, ClientResponse(
                    success=False,
                    message="User id is not in system",
                ).get_response_as_dict(), HttpNoContent)


class AccountResource(ModelResource):
    user = fields.ToOneField(UserResource, "user", related_name="account", full=True)
    city_preference = fields.ManyToManyField(CityResource, "city_preference", related_name="account", full=True,
                                             null=True)

    class Meta:
        allowed_methods = ["get"]
        always_return_data = True
        authentication = Authentication()
        authorization = Authorization()
        queryset = Account.objects.all()
        resource_name = "account"
        filtering = {
            "name": ALL_WITH_RELATIONS
        }


class ProfileResource(ModelResource):
    account = fields.ToOneField(AccountResource, "account", related_name="profile", full=True)
    user = fields.ToOneField(UserResource, "user", related_name="profile", full=True)
    images = fields.ToManyField(
        "new_dawn_server.medias.api.resources.ImageResource",
        "image_set", related_name="profile", full=True, null=True
    )
    answer_questions = fields.ToManyField(
        "new_dawn_server.questions.api.resources.AnswerQuestionResource",
        "answerquestion_set",
        related_name="profile",
        full=True,
        null=True
    )

    class Meta:
        allowed_methods = ["get"]
        # TODO: Remove Authentication once profile main page is developed
        authentication = MultiAuthentication(Authentication(), BasicAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'height': ALL_WITH_RELATIONS,
            'age': ALL_WITH_RELATIONS
        }
        queryset = Profile.objects.all()
        resource_name = "profile"


    def _build_liker_dict(self, likes):
        if likes.count():
            like_obj = likes[likes.count()-1]
            liked_dict = {
                "liked_entity_type": like_obj.entity_type,
                "liked_message": like_obj.message,
            }
            if like_obj.entity_type == EntityType.MAIN_IMAGE.value:
                try:
                    image_obj = Image.objects.get(id=like_obj.entity_id)
                except:
                    image_obj = Image.objects.get(id=1)
                liked_dict["liked_image_url"] = MEDIA_URL + str(image_obj.media)
            if like_obj.entity_type == EntityType.QUESTION_ANSWER.value:
                try:
                    answer_question_obj = AnswerQuestion.objects.get(id=like_obj.entity_id)
                except:
                    answer_question_obj = AnswerQuestion.objects.get(id=1)
                liked_dict["liked_question"] = answer_question_obj.question.question
                liked_dict["liked_answer"] = answer_question_obj.answer
            return liked_dict


    def _get_liker_info(self, bundle):
        # TODO: Refactor this out to become a standalone module
        viewer_id = bundle.request.GET.get('viewer_id')
        user_id = bundle.data["user"].data["id"]
        your_likes = UserAction.objects.filter(
            Q(user_from__id__exact=user_id) 
            & Q(user_to__id__exact=viewer_id) 
            & Q(action_type=ActionType.LIKE.value)
        )
        my_likes = UserAction.objects.filter(
            Q(user_from__id__exact=viewer_id) 
            & Q(user_to__id__exact=user_id) 
            & Q(action_type=ActionType.LIKE.value)
        )
        if your_likes.count():
            bundle.data["liked_info_from_you"] = self._build_liker_dict(your_likes)
            # PENDING DEPRECATION: client should always read liked_info_from_you instead of liked_info
            bundle.data["liked_info"] = self._build_liker_dict(your_likes)
            
        if my_likes.count():
            bundle.data["liked_info_from_me"] = self._build_liker_dict(my_likes)


    def _get_taken_info(self, bundle):
        viewer_id = bundle.request.GET.get('viewer_id')
        user_id = bundle.data["user"].data["id"]
        your_taken = UserAction.objects.filter(
            Q(user_from__id__exact=user_id)
            & Q(user_to__id__exact=viewer_id)
            & Q(action_type=ActionType.REQUEST_TAKEN.value)
        )
        my_taken = UserAction.objects.filter(
            Q(user_from__id__exact=viewer_id)
            & Q(user_to__id__exact=user_id)
            & Q(action_type=ActionType.REQUEST_TAKEN.value)
        )
        if your_taken.count():
            bundle.data["taken_requested_from_you"] = True
        else:
            bundle.data["taken_requested_from_you"] = False

        if my_taken.count():
            bundle.data["taken_requested_from_me"] = True
        else:
            bundle.data["taken_requested_from_me"] = False


    def _get_taken_by_info(self, bundle):
        user_id = bundle.data["user"].data["id"]
        taken_by = UserAction.objects.filter(
            Q(user_from__id__exact=user_id)
            & Q(action_type=ActionType.ALREADY_TAKEN.value)
        )
        if taken_by.count():
            bundle.data["taken_by"] = taken_by.first().user_to


    # Add Answer question fields in Profile Resource
    def dehydrate(self, bundle):
        self._get_liker_info(bundle)
        self._get_taken_info(bundle)
        self._get_taken_by_info(bundle)
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
        allowed_methods = ["post", "put"]
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
    def get_and_save_city_pref(bundle):
        pref_city_list = bundle.data.get("city_preference")
        location_list = []
        if pref_city_list:
            for location in pref_city_list:
                city_pref = CityPreference(
                    city=location['city'],
                    state=location['state'],
                    country=location['country']
                )
                city_pref.save()
                location_list.append(city_pref)
        return location_list

    @staticmethod
    def get_and_save_question(bundle):

        if not Question.objects.filter(question=bundle['question']).exists():
            question = Question(
                question=bundle['question'],
                user_defined=True
            )
            question.save()
        else:
            question = Question.objects.get(question=bundle['question'])
        return question

    @staticmethod
    def get_and_save_answer_question(bundle, user, profile):
        questions_bundle = bundle.data.get("answer_question")
        if questions_bundle:
            for single_question_bundle in questions_bundle:
                question = UserRegisterResource.get_and_save_question(single_question_bundle)
                answer_question = AnswerQuestion(
                    answer=single_question_bundle['answer'],
                    order=single_question_bundle['order'],
                    profile=profile,
                    question=question,
                    user=user
                )
                answer_question.save()

    @staticmethod
    def _get_age(birthday):
        if birthday:
            today = date.today()
            birthday = datetime.datetime.strptime(birthday, "%Y-%m-%d")
            return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
        else:
            return None

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
            city_preference_ls = self.get_and_save_city_pref(bundle)
            account.city_preference.set(city_preference_ls)
            profile = Profile(
                user=user_bundle.obj,
                account=account,
                age=self._get_age(account.birthday),
                **self._get_model_fields_dict(bundle, PROFILE_FIELDS)
            )
            profile.save()

            self.get_and_save_answer_question(bundle, user_bundle.obj, profile)
        return bundle

    def obj_update(self, bundle, skip_errors=False, **kwargs):
        """
        Override obj_update method to edit related models
        """
        with transaction.atomic():
            user_bundle = super(UserRegisterResource, self).obj_update(bundle, **kwargs)
            Profile.objects.get(user=user_bundle.obj).delete()
            Account.objects.get(user=user_bundle.obj).delete()
            account = Account(
                user=user_bundle.obj,
                name=self._get_account_name(user_bundle.obj.first_name, user_bundle.obj.last_name),
                **self._get_model_fields_dict(bundle, ACCOUNT_FIELDS)
            )
            account.save()

            city_preference_ls = self.get_and_save_city_pref(bundle)
            account.city_preference.set(city_preference_ls)
            profile = Profile(
                user=user_bundle.obj,
                account=account,
                **self._get_model_fields_dict(bundle, PROFILE_FIELDS)
            )
            profile.save()

            self.get_and_save_answer_question(bundle, user_bundle.obj, profile)
        return bundle

    def dehydrate(self, bundle):
        # Add extra fields to the response
        bundle.data["username"] = bundle.obj.username
        bundle.data["token"] = bundle.obj.api_key.key
        return bundle
