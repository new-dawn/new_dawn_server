import json
import re

from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDict
from new_dawn_server.medias.models import Image
from new_dawn_server.users.models import Profile
from new_dawn_server.users.api.resources import UserResource
from new_dawn_server.users.api.resources import ProfileResource
from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS

class MultipartResource(object):
    def deserialize(self, request, data, format=None):
        if not format:
             format = request.META.get("CONTENT_TYPE", "application/json")
        if format =="application/x-www-form-urlencoded":
            return request.POST
        if format.startswith("multipart"):
            # Tastypie has no good support for multipart request
            # Have to build our own MultiValueDict from QuerySet
            new_dict = MultiValueDict()
            new_dict.update(json.loads(request.POST.get("data")))
            new_dict.update(request.FILES)
            return new_dict
        return super(MultipartResource, self).deserialize(request, data, format)


class ImageResource(MultipartResource, ModelResource):
    user = fields.ForeignKey(UserResource, "user", related_name="images", full=True)
    # profile = fields.ForeignKey(ProfileResource, "profile", related_name="images", full=True)
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
