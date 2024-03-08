from django.test import TestCase
import datetime
from django.utils import timezone
from .models import Question, Choice
from django.urls import reverse
# Create your tests here.
class QuestionModelTests(TestCase):
    def test_was_published_in_future(self):
        #it should return false for the question which the publication date is in
        #the future.
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published(), False)
    def test_waspublished_old(self):
        time = timezone.now() - datetime.timedelta(days=1,seconds=1)
        old = Question(pub_date=time)
        self.assertIs(old.was_published(),False)

    def test_was_puslished_recently(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent = Question(pub_date=time)
        self.assertIs(recent.was_published(), True)
class ChoiceModelTests(TestCase):
    def is_null_char(self):
        string_returned = Choice(choice_text=null)
        self.assertIs(string_returned.choice_validate(), False)

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        #if no questions exist, an appropiate message is displayed
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls avalable")
        self.assertQuerySetEqual(response.context["lastest_question_list"], [])
    def test_past_question(self):
        #The question with the past pub_date is displayed on the index page
        question = create_question(question_text="Past Question.",days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [question],)
    def test_future(self):
        create_question(question_text="Future_questions", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are  available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])
    def future_and_past(self):
        question  = create_question(question_text="past_question", days=30)
        create_question(question_text="future questions", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["lastest_question_list"], [question],)

    def test_two_past_questions(self):
        question1 = create_question(question_text="past Question 1", days=-30)
        question2 = create_question(question_text="past Question 2", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["lastest_question_list"],[question2, question1],
        )
class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        future_question = create_question(question_text="Future question", days=5)
        url = reverse("polls:details", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question(question_text="past question.",days=-5)
        url = reverse("polls:details",args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)