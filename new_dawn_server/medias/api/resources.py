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
        if format == "application/x-www-form-urlencoded":
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
    media = fields.FileField(attribute="media")

    class Meta:
        always_return_data = True
        authentication = Authentication()
        authorization = Authorization()
        allowed_methods = ["get", "post"]
        filtering = {
            "user": ALL_WITH_RELATIONS
        }
        ordering = ["order"]
        queryset = Image.objects.all()
        resource_name = "image"

    def obj_create(self, bundle, **kwargs):
        user_uri = bundle.data.get("user")
        user_id = int(user_uri.split("/")[-2])
        user_obj = User.objects.get(id=user_id)
        img_bundle = super(ImageResource, self).obj_create(bundle, user=user_obj, media=bundle.data["media"])
        profile_obj = Profile.objects.get(user_id=user_id)
        img_bundle.obj.profile = profile_obj
        img_bundle.obj.save()
        return bundle
