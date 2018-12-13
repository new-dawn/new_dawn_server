from django.contrib.auth.models import User
from django.test import TestCase
from new_dawn_server.questions.models import AnswerQuestion, Question


class QuestionTest(TestCase):
    def setUp(self):
        Question.objects.create(
            question="How are you doing?",
            sample_answer="Very Good",
        )

    def test_question(self):
        test_question_case = Question.objects.first()
        self.assertEqual(test_question_case.question, "How are you doing?")
        self.assertEqual(test_question_case.sample_answer, "Very Good")


class AnswerQuestionTest(TestCase):
    def setUp(self):
        Question.objects.create(
            question="How are you doing?",
            sample_answer="Very Good",
        )

        self.user = User.objects.create()
        self.answers = ["Good Good Good", "Good Good Bad"]

        AnswerQuestion.objects.create(
            answer=self.answers[0],
            order=1,
            question=Question.objects.first(),
            user=self.user
        )

        AnswerQuestion.objects.create(
            answer=self.answers[1],
            order=2,
            question=Question.objects.first(),
            user=self.user
        )

    def test_get_QA_from_user(self):
        test_user = User.objects.first()
        # Use .filter instead of .get since one user can have multiple AnswerQuestion
        test_qa = AnswerQuestion.objects.filter(user=test_user)[0]
        self.assertEqual(test_qa.question.question, "How are you doing?")
        self.assertEqual(test_qa.answer, "Good Good Good")
        self.assertEqual(test_qa.order, 1)
        self.assertEqual(test_qa.question.sample_answer, "Very Good")

    def test_get_answers_from_question(self):
        test_question = Question.objects.first()
        # Access reverse foreign key relation via _set suffix
        test_answers = test_question.answerquestion_set.all()
        for i, test_answer in enumerate(test_answers):
            self.assertEqual(test_answer.answer, self.answers[i])
