from django.conf.urls import url
from new_dawn_server.locations.constants.city_constants import US_CITY_MAPPING, COUNTRY_LIST
from new_dawn_server.locations.constants.college_constants import COLLEGE_NAMES
from new_dawn_server.locations.models import CityPreference
from new_dawn_server.modules.client_response import ClientResponse
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.http import HttpBadRequest
from tastypie.resources import ModelResource


class CityResource(ModelResource):
    class Meta:
        always_return_data = True
        authentication = Authentication()
        authorization = Authorization()
        allowed_methods = ["get", "post"]
        filtering = {
                        'country': "exact",
                        'state': "exact"
                    },
        queryset = CityPreference.objects.all()
        resource_name = "city_preference"

    def prepend_urls(self):
        return [
            url(r"^city_preference/get_country_list/$", self.wrap_view("get_country_list"),
                name="api_get_country_list"),
            url(r"^city_preference/get_state_for_country/$", self.wrap_view("get_state_for_country"),
                name="api_get_state_for_country"),
            url(r"^city_preference/get_city_for_state/$", self.wrap_view("get_city_for_state"),
                name="api_get_city_for_country"),
            url(r"^city_preference/get_college_list/$", self.wrap_view("get_college_list"),
                name="api_get_college_list")
        ]

    def get_country_list(self, request, **kwargs):
        # TODO: Complete country list
        self.method_check(request, allowed=["get"])
        return self.create_response(request,
                                    ClientResponse(
                                        success=True,
                                        message="Country list sent",
                                        country_list=list(COUNTRY_LIST.keys())
                                    ).get_response_as_dict()
                                    )

    def get_state_for_country(self, request, **kwargs):
        self.method_check(request, allowed=["get"])
        country = request.GET.get("country", "")
        if country:
            # TODO: Change to more complete hierarchical country mapping
            return self.create_response(request,
                                        ClientResponse(
                                            success=True,
                                            message="State list sent",
                                            state_list=COUNTRY_LIST[country])
                                        .get_response_as_dict()
                                        )

        else:
            return self.create_response(request, ClientResponse(
                success=False,
                message="Not given country name",
            ).get_response_as_dict(), HttpBadRequest)

    def get_city_for_state(self, request, **kwargs):
        self.method_check(request, allowed=["get"])
        country = request.GET.get("country", "")
        state = request.GET.get("state", "")
        if country and state:
            if country == "United States":
                # TODO: Capture not match error
                return self.create_response(request,
                                            ClientResponse(
                                                success=True,
                                                message="City list sent",
                                                city_list=list(US_CITY_MAPPING[state])
                                            ).get_response_as_dict()
                                            )
        else:
            return self.create_response(request, ClientResponse(
                success=False,
                message="Not given country/City name",
            ).get_response_as_dict(), HttpBadRequest)

    def get_college_list(self, request, **kwargs):
        # TODO: Complete college list
        self.method_check(request, allowed=["get"])
        return self.create_response(request,
                                    ClientResponse(
                                        success=True,
                                        message="College list sent",
                                        college_list=COLLEGE_NAMES
                                    ).get_response_as_dict())
