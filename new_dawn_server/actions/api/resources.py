from new_dawn_server.actions.models import UserAction
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


class UserActionResource(ModelResource):
    user_account_from = fields.ForeignKey(AccountResource, "user_account_from", related_name="user_action", full=True)
    user_account_to = fields.ForeignKey(AccountResource, "user_account_to", related_name="user_action",
                                        full=True)

    class Meta:
        always_return_data = True
        authentication = Authentication()
        authorization = Authorization()
        allowed_methods = ["get", "post"]
        queryset = UserAction.objects.all()
        resource_name = "user_action"
        filtering = {
            "user_account_from": ALL_WITH_RELATIONS,
            "user_account_to": ALL_WITH_RELATIONS,
        }

    def hydrate_user_account_from(self, bundle):
        bundle.data["user_account_from"] = "/api/v1/account/" + bundle.data["user_account_from"] + "/"
        return bundle

    def hydrate_user_account_to(self, bundle):
        bundle.data["user_account_to"] = "/api/v1/account/" + bundle.data["user_account_to"] + "/"
        return bundle
