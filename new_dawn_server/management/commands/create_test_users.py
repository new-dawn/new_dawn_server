import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from new_dawn_server.medias.models import Image
from new_dawn_server.questions.models import Question, AnswerQuestion
from new_dawn_server.users.models import Account, Profile


class Command(BaseCommand):

    def create_test_image(self, user, profile, caption, url, order):
        img = Image.objects.create(
            caption=caption,
            media=url,
            order=order,
            profile=profile, 
            update_time="2018-01-01",
            user=user,
        )
        return img

    def create_test_answer_questions(self, user, profile, question, answer, order):
        question_obj = Question.objects.get_or_create(question=question)
        answer = AnswerQuestion.objects.create(
            answer=answer, 
            order=order,
            profile=profile,
            question=question_obj[0],
            user=user,
        )
        return answer

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
        test_profile.image_set.add(self.create_test_image(test_user, test_profile, "Test Image 12", "images/testgirl2.jpg", 1))
        test_profile.image_set.add(self.create_test_image(test_user, test_profile, "Test Image 13", "images/testgirl3.jpg", 2))
        test_profile.image_set.add(self.create_test_image(test_user, test_profile, "Test Image 14", "images/testgirl4.jpg", 3))
        test_profile.image_set.add(self.create_test_image(test_user, test_profile, "Test Image 15", "images/testgirl5.jpg", 4))
        
        test_profile.answerquestion_set.add(
            self.create_test_answer_questions(test_user, test_profile, "What's your best movie?", "Inception", 0))
        test_profile.answerquestion_set.add(
            self.create_test_answer_questions(test_user, test_profile, "What's your first toy?", "A Doll", 1))
        test_profile.answerquestion_set.add(
            self.create_test_answer_questions(test_user, test_profile, "What's your total GPA?", "3.92", 2))

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
        test_profile.image_set.add(self.create_test_image(test_user, test_profile, "Test Image 21", "images/testgirl6.jpeg", 0))
        test_profile.image_set.add(self.create_test_image(test_user, test_profile, "Test Image 22", "images/testgirl7.jpg", 1))
        test_profile.image_set.add(self.create_test_image(test_user, test_profile, "Test Image 23", "images/testgirl8.jpg", 2))
        test_profile.image_set.add(self.create_test_image(test_user, test_profile, "Test Image 24", "images/testgirl9.jpg", 3))

        test_profile.answerquestion_set.add(
            self.create_test_answer_questions(test_user, test_profile, "What's your 2019 resolution?", "Build a tower", 0))
        test_profile.answerquestion_set.add(
            self.create_test_answer_questions(test_user, test_profile, "Who's your icon?", "Kevin", 1))
        test_profile.answerquestion_set.add(
            self.create_test_answer_questions(test_user, test_profile, "Where were you born?", "New York", 2))

    def create_test_user_3(self):
        # Always re-create the test user
        User.objects.filter(username="testuser3").delete()
        test_user = User.objects.create_user(
            first_name="Thomas",
            last_name="Chen",
            username="testuser3",
            email="test3@gmail.com",
            password="testuser3"
        )
        test_account = Account.objects.create(
            birthday="1991-05-11",
            creation_date="2018-01-02",
            gender="M",
            name="test_user_3",
            phone_number="1111111111",
            user=test_user,
        )
        test_profile = Profile.objects.create(
            account=test_account,
            degree="Grad",
            description="Great",
            drink="A few",
            employer="GG",
            height=180,
            hometown="China",
            job_title="Reader",
            profile_photo_url="images/testnyu.JPG",
            school="CMU",
            smoke="Socially",
            update_time="2018-01-02",
            user=test_user,
        )
        test_profile.image_set.add(
            self.create_test_image(test_user, test_profile, "Test Image 21", "images/testman1.jpg", 0))
        test_profile.image_set.add(
            self.create_test_image(test_user, test_profile, "Test Image 22", "images/testman2.jpg", 1))
        test_profile.image_set.add(
            self.create_test_image(test_user, test_profile, "Test Image 23", "images/testman3.jpg", 2))
        test_profile.image_set.add(
            self.create_test_image(test_user, test_profile, "Test Image 24", "images/testman4.jpg", 3))

        test_profile.answerquestion_set.add(
            self.create_test_answer_questions(test_user, test_profile, "What's your 2019 resolution?", "Build a tower",
                                              0))
        test_profile.answerquestion_set.add(
            self.create_test_answer_questions(test_user, test_profile, "How are you?", "Good", 1))
        test_profile.answerquestion_set.add(
            self.create_test_answer_questions(test_user, test_profile, "Who's your favorite rapper", "Kanye", 2))

    def handle(self, *args, **options):
        # User 1 is super user
        print("Create Test User 2")
        self.create_test_user_1()
        print("Create Test User 3")
        self.create_test_user_2()
        print("Create Test User 4")
        self.create_test_user_3()