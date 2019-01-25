from new_dawn_server.actions.models import UserToUserActionMetadata, Like
from new_dawn_server.users.api.resources import AccountResource
from tastypie import fields
from tastypie.authentication import (
    ApiKeyAuthentication,
    Authentication,
    BasicAuthentication,
    MultiAuthentication
)
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS


class ActionMetaResource(ModelResource):
    user_account_from = fields.ForeignKey(AccountResource, "user_account_from", related_name="user_action", full=True)
    user_account_to = fields.ForeignKey(AccountResource, "user_account_to", related_name="user_action",
                                        full=True)

    class Meta:
        always_return_data = True
        authentication = Authentication()
        authorization = Authorization()
        allowed_methods = ["get", "post"]
        queryset = UserToUserActionMetadata.objects.all()
        resource_name = "user_action"


class LikeResouce(ModelResource):
    like = fields.ForeignKey(ActionMetaResource, "like", related_name="like",
                             full=True)

    class Meta:
        always_return_data = True
        authentication = Authentication()
        authorization = Authorization()
        allowed_methods = ["get", "post"]
        queryset = Like.objects.all()
        resource_name = "like"
