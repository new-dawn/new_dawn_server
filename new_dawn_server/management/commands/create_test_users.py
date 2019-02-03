import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from new_dawn_server.medias.models import Image
from new_dawn_server.users.models import Account, Profile


class Command(BaseCommand):

    def create_test_image(self, user, profile, caption, url, order):
        img = Image.objects.create(
            caption=caption,
            media=url,
            order=order,
            profile=profile, 
            update_time = "2018-01-01",
            user=user,
        )
        return img

    def create_test_user_1(self):
        # Always re-create the test user
        User.objects.filter(username="testuser1").delete()
        test_user = User.objects.create_user(
            first_name="Tracy",
            last_name="Wang",
            username="testuser1", 
            email="test@gmail.com", 
            password="testuser1"
        )
        test_account = Account.objects.create(
            birthday="2000-03-01",
            creation_date="2018-01-01",
            gender="M",
            name="test_user_1",
            phone_number="333333333",
            user=test_user,
        )
        test_profile = Profile.objects.create(
            account=test_account,
            degree="Undergrad",
            description="Nothing to say",
            drink="A lot",
            employer="MM",
            height=180,
            hometown="China",
            job_title="Engineer",
            profile_photo_url="images/testcat.JPG",
            school="NYU",
            smoke="Socially",
            update_time="2018-01-01",
            user=test_user,
        )
        test_profile.image_set.add(self.create_test_image(test_user, test_profile, "Test Image 11", "images/testgirl1.jpeg", 0))
        test_profile.image_set.add(self.create_test_image(test_user, test_profile, "Test Image 12", "images/testgirl2.jpg", 0))
        test_profile.image_set.add(self.create_test_image(test_user, test_profile, "Test Image 13", "images/testgirl3.jpg", 0))
        # TODO: Create some question answers here

    def create_test_user_2(self):
        # Always re-create the test user
        User.objects.filter(username="testuser2").delete()
        test_user = User.objects.create_user(
            first_name="Max",
            last_name="Zhang",
            username="testuser2", 
            email="test2@gmail.com", 
            password="testuser2"
        )
        test_account = Account.objects.create(
            birthday="1991-01-11",
            creation_date="2018-01-01",
            gender="F",
            name="test_user_2",
            phone_number="1111111111",
            user=test_user,
        )
        test_profile = Profile.objects.create(
            account=test_account,
            degree="Grad",
            description="Great",
            drink="A few",
            employer="MM",
            height=160,
            hometown="China",
            job_title="Reader",
            profile_photo_url="images/testnyu.JPG",
            school="CMU",
            smoke="Never",
            update_time="2018-01-01",
            user=test_user,
        )
        test_profile.image_set.add(self.create_test_image(test_user, test_profile, "Test Image 21", "images/testgirl4.jpg", 0))
        test_profile.image_set.add(self.create_test_image(test_user, test_profile, "Test Image 22", "images/testgirl5.jpg", 0))
        # TODO: Create some question answers here

    def handle(self, *args, **options):
        print("Create Test User 1")
        self.create_test_user_1()
        print("Create Test User 2")
        self.create_test_user_2()