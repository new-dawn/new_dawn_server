"""new_dawn_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from new_dawn_server.actions.api.resources import (
    UserActionResource
)
from new_dawn_server.locations.api.resources import (
    CityResource
)
from new_dawn_server.medias.api.resources import (
    ImageResource
)
from new_dawn_server.questions.api.resources import (
    AnswerQuestionResource,
    QuestionResource
)
from new_dawn_server.users.api.resources import (
    AccountResource,
    UserRegisterResource,
    UserResource,
    ProfileResource,
)
from tastypie.api import Api

# Tastypie API v1 Register
v1_api = Api(api_name='v1')
v1_api.register(AccountResource())
v1_api.register(AnswerQuestionResource())
v1_api.register(CityResource())
v1_api.register(ImageResource())
v1_api.register(ProfileResource())
v1_api.register(QuestionResource())
v1_api.register(UserActionResource())
v1_api.register(UserRegisterResource())
v1_api.register(UserResource())

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(v1_api.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
