import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question
from django.urls import reverse
from typing import Any, Dict

# Create your tests here.


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self) -> None:
        """Test that a question with a future publish date is not was_published_recently"""
        question_time = timezone.now() + datetime.timedelta(days=1)
        future_question = Question(pub_date=question_time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self) -> None:
        question_time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        future_question = Question(pub_date=question_time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self) -> None:
        question_time = timezone.now() - datetime.timedelta(hours=1)
        future_question = Question(pub_date=question_time)
        self.assertIs(future_question.was_published_recently(), True)


def create_question(question_text:str, days:int) -> Any:
    pub_date = timezone.now() + datetime.timedelta(days=days)
    ret = Question.objects.create(question_text=question_text, pub_date=pub_date)
    # reveal_type(ret) # -> "Any"
    return ret


class QuestionIndexViewTests(TestCase):
    def test_past_question(self) -> None:
        question = create_question("Past question", -30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])

    def test_future_question(self) -> None:
        question = create_question("Future question", 1)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_and_past_question(self) -> None:
        create_question("Future question", 1)
        question = create_question("Past question", -1)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])

    def test_two_past_questions(self) -> None:
        question1 = create_question("Past question 1", -1)
        question2 = create_question("Past question 2", -1)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"], [question2, question1]
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self) -> None:
        question = create_question("Future question", 1)
        response = self.client.get(reverse("polls:detail", args=(question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_future_question2(self) -> None:
        question = create_question("Future question", -1)
        response = self.client.get(reverse("polls:detail", args=(question.id,)))
        self.assertContains(response, question.question_text)
