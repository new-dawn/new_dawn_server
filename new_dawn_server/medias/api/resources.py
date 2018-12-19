from new_dawn_server.medias.models import Image
from new_dawn_server.users.api.resources import UserResource
from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS

class ImageResource(ModelResource):
    media = fields.FileField(attribute="media", blank=True, null=True)
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
