import json
import os
import re

from django.contrib.auth.models import User
from django.db.models.fields.files import ImageFieldFile
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
        with open("media/images/test.png", "rb") as photo_file:
            test_data_json = json.dumps(self.test_data)
            # The full data should have a json serialized dict
            # and an actual File instance
            full_data = {
                "data": test_data_json, 
                "media": photo_file,
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
            self.assertEquals(response.status_code, 201)

            # Test upload success: basic info
            self.assertEquals(Image.objects.count(), 1)
            image = Image.objects.all()[0]
            self.assertEquals(image.caption, "good")
            self.assertEquals(image.order, 1)
            self.assertEquals(
                image.user, User.objects.get(username="test-user"))

            # Test upload success: image file
            file = image.media
            self.assertTrue(isinstance(file, ImageFieldFile))
            self.assertTrue(file.name.startswith("images/test_"))
            self.assertTrue(file.name.endswith(".png"))
            self.assertTrue(file.url.startswith("/media/images/test_"))

            # Remove the uploaded file
            os.remove(file.path)



