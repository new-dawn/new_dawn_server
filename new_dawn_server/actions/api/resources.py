from django.conf.urls import url
from django.contrib.auth.models import User
from django.db.models import Q
from new_dawn_server.actions.constants import (
    ActionType, EntityType, END_USER_ID, END_USER_FIRSTNAME, END_USER_LASTNAME, END_USER_IMAGE_URL
)
from new_dawn_server.actions.models import UserAction
from new_dawn_server.modules.client_response import ClientResponse
from new_dawn_server.pusher.chat_service import ChatService
from new_dawn_server.pusher.notification_service import NotificationService
from new_dawn_server.medias.models import Image
from new_dawn_server.users.api.resources import UserResource
from new_dawn_server.settings import MEDIA_URL
from tastypie import fields
from tastypie.authentication import (
    ApiKeyAuthentication,
    Authentication,
    BasicAuthentication,
    MultiAuthentication
)
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS


class UserActionResource(ModelResource):
    user_from = fields.ForeignKey(UserResource, "user_from", related_name="user_action", full=True)
    user_to = fields.ForeignKey(UserResource, "user_to", related_name="user_action",
                                full=True)

    class Meta:
        always_return_data = True
        authentication = Authentication()
        authorization = Authorization()
        allowed_methods = ["get", "post"]
        queryset = UserAction.objects.all()
        resource_name = "user_action"
        filtering = {
            "user_from": ALL_WITH_RELATIONS,
            "user_to": ALL_WITH_RELATIONS,
            "message": ALL_WITH_RELATIONS,
            "action_type": ALL_WITH_RELATIONS
        }

    @staticmethod
    def create_match(user_from_id, user_to_id):
        user_from = User.objects.get(username=user_from_id)
        user_to = User.objects.get(username=user_to_id)
        UserAction(
            user_from=user_from,
            user_to=user_to,
            action_type=ActionType.MATCH.value,
            entity_id=0,
            entity_type=EntityType.NONE.value
        ).save()
        UserAction(
            user_from=user_to,
            user_to=user_from,
            action_type=ActionType.MATCH.value,
            entity_id=0,
            entity_type=EntityType.NONE.value
        ).save()
        NotificationService().send_notification([str(user_from_id), str(user_to_id)], message="You are matched")

    def obj_create(self, bundle, **kwargs):
        super(UserActionResource, self).obj_create(bundle).obj.save()
        if bundle.data.get("action_type") == ActionType.LIKE.value:
            NotificationService().send_notification([str(bundle.data.get("user_to_id"))], message="You are liked")
            if UserAction.objects.filter(user_to__username=bundle.data.get("user_from_id"),
                                         user_from__username=bundle.data.get("user_to_id"),
                                         action_type=ActionType.LIKE.value).exists():
                self.create_match(bundle.data.get("user_from_id"), bundle.data.get("user_to_id"))
        return bundle

    def prepend_urls(self):
        return [
            url(r"^user_action/send_message/$", self.wrap_view("send_message"), name="api_send_message"),
            url(r"^user_action/get_messages/$", self.wrap_view("get_messages"), name="api_get_messages"),
        ]

    def construct_resource_uri(self, username):
        user = User.objects.get(username=username)
        return "api/v1/user/" + str(user.id) + "/"

    def hydrate_user_from(self, bundle):
        bundle.data["user_from_id"] = bundle.data["user_from"]
        bundle.data["user_from"] = self.construct_resource_uri(bundle.data["user_from"])
        return bundle

    def hydrate_user_to(self, bundle):
        bundle.data["user_to_id"] = bundle.data["user_to"]
        bundle.data["user_to"] = self.construct_resource_uri(bundle.data["user_to"])
        return bundle

    def send_message(self, request, **kwargs):
        # Send message action consists of two parts
        # 1. Store message in backend
        # 2. Return channel id that client can listen to update the chat view in real-time
        self.method_check(request, allowed=["post"])
        data = self.deserialize(request, request.body, format=request.META.get("CONTENT_TYPE", "application/json"))
        user_from = data.get("user_from", "")
        user_to = data.get("user_to", "")
        message = data.get("message", "")
        chat_service = ChatService(user_from, user_to)
        chat_service.send(message)
        message_action = UserAction(
            action_type=ActionType.MESSAGE.value,
            entity_id=1,
            entity_type=EntityType.NONE.value,
            user_from=User.objects.get(username=user_from),
            user_to=User.objects.get(username=user_to),
            message=message
        )
        message_action.save()
        return self.create_response(
            request, ClientResponse(
                success=True,
                message="Message Sent",
            ).get_response_as_dict())

    def build_message_tuple(self, message_action):
        return {
            "user_from_id": message_action.user_from.username,
            "user_from_firstname": message_action.user_from.first_name,
            "user_from_lastname": message_action.user_from.last_name,
            "user_to_id": message_action.user_to.username,
            "user_to_firstname": message_action.user_to.first_name,
            "user_to_lastname": message_action.user_to.last_name,
            "message": message_action.message,
            "message_id": message_action.id
        }

    def build_end_user_metainfo(self, user_obj):
        img = Image.objects.filter(user__username=user_obj.username)
        return {
            END_USER_IMAGE_URL: MEDIA_URL + str(Image.objects.filter(user__username=user_obj.username)[0].media) if len(
                img) > 0 else "",
            END_USER_FIRSTNAME: user_obj.first_name,
            END_USER_LASTNAME: user_obj.last_name,
            END_USER_ID: user_obj.username,
        }

    def build_message_response(self, main_actor_id, matches, messages):
        """
        Return a message dict where the key is the end user's id,
        value is a list of (user_from, user_to, message) tuple between
        current user and the end user
        """
        result = {}
        # Keep track of the basic info of each end user
        end_user_info = {}
        # Bootstrap the message list for each matched end user
        for match_action in matches:
            if str(match_action.user_from.username) != main_actor_id:
                key = match_action.user_from.username
                if key not in result:
                    result[key] = []
                    end_user_info[key] = self.build_end_user_metainfo(match_action.user_from)
            if str(match_action.user_to.username) != main_actor_id:
                key = match_action.user_to.username
                if key not in result:
                    result[key] = []
                    end_user_info[key] = self.build_end_user_metainfo(match_action.user_to)

        # Iterate through the list of messages
        for message_action in messages:
            if str(message_action.user_from.username) != main_actor_id:
                key = message_action.user_from.username
                # The key should already in the result. Otherwise the two users are
                # not matched with each other
                try:
                    result[key].append(self.build_message_tuple(message_action))
                except KeyError:
                    print(
                        f"MessageRetrievalError: User {main_actor_id} and user {message_action.user_from.username} are not connected")

            if str(message_action.user_to.username) != main_actor_id:
                key = message_action.user_to.username
                # The key should already in the result. Otherwise the two users are
                # not matched with each other
                try:
                    result[key].append(self.build_message_tuple(message_action))
                except KeyError:
                    print(
                        f"MessageRetrievalError: User {main_actor_id} and user {message_action.user_to.username} are not connected")
        return [
            {
                END_USER_ID: end_user_info[key][END_USER_ID],
                END_USER_FIRSTNAME: end_user_info[key][END_USER_FIRSTNAME],
                END_USER_LASTNAME: end_user_info[key][END_USER_LASTNAME],
                END_USER_IMAGE_URL: end_user_info[key][END_USER_IMAGE_URL],
                "messages": value,
            }
            for key, value in result.items()
        ]

    def get_messages(self, request, **kwargs):
        # Get messages action fetch all messages that
        # 1. Sent by the current user
        # 2. Received by the user that the current user matched with
        # 3. Keyed by received user's Username
        # 4. Sorted by action creation time
        self.method_check(request, allowed=["get"])
        # TODO: Authenticate the user before allowing GET to go through
        matches = UserAction.objects.filter(
            (Q(user_from__username__exact=request.GET["user_from"])
             & Q(action_type=ActionType.MATCH.value))
            |
            (Q(user_to__username__exact=request.GET["user_from"])
             & Q(action_type=ActionType.MATCH.value))
        ).order_by("update_time")
        messages = UserAction.objects.filter(
            (Q(user_from__username__exact=request.GET["user_from"])
             & Q(action_type=ActionType.MESSAGE.value))
            |
            (Q(user_to__username__exact=request.GET["user_from"])
             & Q(action_type=ActionType.MESSAGE.value))
        ).order_by("update_time")
        return self.create_response(request, ClientResponse(
            success=True,
            message="Message Get Successful",
            objects=self.build_message_response(request.GET["user_from"], matches, messages)
        ).get_response_as_dict())
