from new_dawn_server.locations.models import CityPreference
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource


class CityResource(ModelResource):
    class Meta:
        always_return_data = True
        authorization = Authorization()
        allowed_methods = ["get", "post"]
        queryset = CityPreference.objects.all()
        resource_name = "city_preference"
