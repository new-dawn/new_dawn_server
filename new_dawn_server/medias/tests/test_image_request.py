import json
import os
import re

from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.db.models.fields.files import ImageFieldFile
from django.test import TestCase
from new_dawn_server.medias.models import Image
from new_dawn_server.users.models import Profile
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

            # Test GET API: will only get media path instead of file itself
            res = self.api_client.get("/api/v1/image/", format="json")
            res_data = json.loads(res.content)
            image_data = res_data['objects'][0]
            self.assertEquals(image_data["caption"], "good")
            self.assertEquals(image_data["order"], 1)
            self.assertTrue(image_data["media"].startswith("/media/images/test_"))
            user_data = image_data["user"]
            self.assertEquals(user_data["username"], "test-user")

            # Remove the uploaded file
            try:
                os.remove(file.path)
            except OSError:
                pass

    def test_upload_image_with_simpleupload(self):

        image = SimpleUploadedFile("media/images/test.png", b"file_content", content_type="image/png")
        test_data_json = json.dumps(self.test_data)
        # The full data should have a json serialized dict
        # and an actual File instance
        full_data = {
            "data": test_data_json,
            "media": image,
        }
        response = self.client.post(
            '/api/v1/image/',
            data=full_data,
        )
        self.assertEquals(response.status_code, 201)

        # Test same tests written above
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
        res = self.api_client.get("/api/v1/image/", format="json")
        res_data = json.loads(res.content)
        image_data = res_data['objects'][0]
        self.assertEquals(image_data["caption"], "good")
        self.assertEquals(image_data["order"], 1)
        self.assertTrue(image_data["media"].startswith("/media/images/test_"))
        user_data = image_data["user"]
        self.assertEquals(user_data["username"], "test-user")

        # Test User and Profile fields exist
        self.assertEquals(Image.objects.first().profile, Profile.objects.get(user__username="test-user"))
        self.assertEquals(Image.objects.first().user, User.objects.get(username="test-user"))

        # Remove the uploaded file
        try:
            os.remove(file.path)
        except OSError:
            pass

    def test_get_multiple_images(self):
        register_arguments_2 = {
            "first_name": "test2",
            "last_name": "user2",
            "username": "test-user2",
            "password": "test-pwd2",
        }
        self.api_client.post(
            "/api/v1/register/", format="json", data=register_arguments_2)
        test_data_2 = {
            "caption": "good",
            "order": 2,
            "user": "/api/v1/user/2/",
        }
        # User 2 post "order 2" image
        with open("media/images/testman1.jpg", "rb") as photo_file:
            test_data_json = json.dumps(test_data_2)
            full_data = {
                "data": test_data_json,
                "media": photo_file,
            }
            response = self.client.post(
                '/api/v1/image/',
                data=full_data,
            )
        test_data_1 = {
            "caption": "good",
            "order": 1,
            "user": "/api/v1/user/2/",
        }
        # User 2 post "order 1" image
        with open("media/images/test.png", "rb") as photo_file:
            test_data_json = json.dumps(test_data_1)
            full_data = {
                "data": test_data_json,
                "media": photo_file,
            }
            response = self.client.post(
                '/api/v1/image/',
                data=full_data,
            )
        test_data_3 = {
            "caption": "good",
            "order": 1,
            "user": "/api/v1/user/1/",
        }
        # User 1 post "order 1" image
        with open("media/images/testman2.jpg", "rb") as photo_file:
            test_data_json = json.dumps(test_data_3)
            full_data = {
                "data": test_data_json,
                "media": photo_file,
            }
            response = self.client.post(
                '/api/v1/image/',
                data=full_data,
            )

        res = self.api_client.get("/api/v1/image/", format="json")
        res_data = json.loads(res.content)
        data = res_data["objects"]

        # Verify the ordering of image request
        self.assertEqual(data[0]["user"]["id"], 1)
        self.assertEqual(data[1]["user"]["id"], 2)
        self.assertEqual(data[2]["user"]["id"], 2)
        self.assertEqual(data[0]["order"], 1)
        self.assertEqual(data[1]["order"], 1)
        self.assertEqual(data[2]["order"], 2)

        images = Image.objects.all()
        for image in images:
            file = image.media
            try:
                os.remove(file.path)
            except OSError:
                pass

        res = self.api_client.get("/api/v1/profile/?user__id=2", format="json")
        res_data = json.loads(res.content)
        data = res_data["objects"]
        self.assertEqual(data[0]["images"][0]["order"], 1)
        self.assertEqual(data[0]["images"][1]["order"], 2)
        # Verify the ordering of images in user profile

