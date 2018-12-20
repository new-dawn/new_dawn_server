import json
import re

from django.contrib.auth.models import User
from new_dawn_server.medias.models import Image
from new_dawn_server.users.models import Profile
from new_dawn_server.users.api.resources import UserResource
from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS

class MultipartResource(object):
    def deserialize(self, request, data, format=None):
        # Tastypie has no good support for multipart request
        # have to override the deserialize function as a whole
        if not format:
             format = request.META.get("CONTENT_TYPE", "application/json")
        if format =="application/x-www-form-urlencoded":
            return request.POST
        if format.startswith("multipart"):
            data = json.loads(request.POST.get("data"))
            data.update(request.FILES["media"])
            return data
        return super(MultipartResource, self).deserialize(request, data, format)


class ImageResource(MultipartResource, ModelResource):
    user = fields.ToOneField(UserResource, "user", related_name="image", full=True)
    media = fields.FileField(attribute="media")
    class Meta:
        always_return_data = True
        authentication = Authentication()
        authorization = Authorization()
        allowed_methods = ["get", "post"]
        filtering = {
        	"user": ALL_WITH_RELATIONS
        }
        queryset = Image.objects.all()
        resource_name = "image"
