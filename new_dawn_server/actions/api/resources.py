from django.conf.urls import url
from django.contrib.auth.models import User
from new_dawn_server.actions.constants import ActionType, EntityType
from new_dawn_server.actions.models import UserAction
from new_dawn_server.modules.client_response import ClientResponse
from new_dawn_server.pusher.chat_service import ChatService
from new_dawn_server.users.api.resources import UserResource
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
        }

    def prepend_urls(self):
        return [
            url(r"^user_action/send_message/$", self.wrap_view("send_message"), name="api_send_message"),
        ]

    def hydrate_user_from(self, bundle):
        bundle.data["user_from"] = "/api/v1/user/" + bundle.data["user_from"] + "/"
        return bundle

    def hydrate_user_to(self, bundle):
        bundle.data["user_to"] = "/api/v1/user/" + bundle.data["user_to"] + "/"
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
            user_from=User.objects.get(id=int(user_from)),
            user_to=User.objects.get(id=int(user_to)),
            message=message
        )
        message_action.save()
        return self.create_response(
                request, ClientResponse(
                    success=True,
                    message="Message Sent",
                ).get_response_as_dict())


