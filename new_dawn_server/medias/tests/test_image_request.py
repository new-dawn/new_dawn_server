import base64
import json
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from new_dawn_server.medias.models import Image
from tastypie.test import ResourceTestCaseMixin



class ImageTest(ResourceTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.register_arguments = {
            "first_name": "test",
            "last_name": "user",
            "username": "test-user",
            "password": "test-pwd",
        }
        # Register a regular user
        self.api_client.post(
            "/api/v1/register/", format="json", data=self.register_arguments)

        self.test_data = {
            "caption": "good",
            "order": 1,
            "user": "/api/v1/user/1/",
        }

    def test_upload_photo_multipart(self):
        # Expect front-end to send base64 encoded image binary
        with open("media/images/test.png", "rb") as photo:
            test_data_json = json.dumps(self.test_data)
            test_photo_encoded = base64.b64encode(photo.read())

            # Expect front-end to encode the media via base64
            full_data = {
                "data": test_data_json, 
                "media": photo,
            }

            # Data should be of the form:
            # {'data': ['{"caption": "good", "order": 1, "user": "/api/v1/user/1/"}'], 
            # 'media': [<InMemoryUploadedFile: test.png (image/png)>]}
            
            # Have to use Django test client since tastypie
            # doesn't support multipart request
            response = self.client.post(
                '/api/v1/image/',
                data=full_data,
            )
            photo.close()
            self.assertEquals(response.status_code, 201)

            res = self.api_client.get("/api/v1/image/", format="json")
            res_data = json.loads(res.content)
            for k, v in res_data['objects'][0].items():
                if k == "user":
                    self.assertTrue(v['username'] == "test-user")


