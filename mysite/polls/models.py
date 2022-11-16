from datetime import datetime, timedelta
from django.utils import timezone
from django.db import models
from django.db.models import F
from django.contrib import admin
# from traitlets import Bool
from typing import Any
# Create your models here.


class Question(models.Model):
    question_text: models.CharField[str, str] = models.CharField(max_length=512)
    # question_text: CharField[str, str] = models.CharField(max_length=512)
    # pub_date = models.DateTimeField("date_published")
    # reveal_type(pub_date) # -> django.db.models.fields.DateTimeField[Any, Any]
    pub_date: models.fields.DateTimeField[Any, Any] = models.DateTimeField("date_published")

    # pub_date : DateTimeField = models.DateTimeField("date_published")

    def __str__(self) -> str:
        return self.question_text

    @admin.display(boolean=True,
                   ordering='pub_date',
                   description='Published recently')
    def was_published_recently(self) -> bool:
        now = timezone.now()
        recently = bool(self.pub_date >= timezone.now() - timedelta(days=1)
                and self.pub_date <= now
                )
        # reveal_type(recently) # -> "builtins.bool"
        return recently


class Choice(models.Model):
    question: models.fields.related.ForeignKey[Any, Any] = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="choice_set"
    )
    # reveal_type(question) # -> django.db.models.fields.related.ForeignKey[Any, Any]
    choice_text: models.fields.CharField[Any, Any] = models.CharField(max_length=512)
    # reveal_type(choice_text)  # -> django.db.models.fields.CharField[Any, Any]
    votes: models.fields.IntegerField[Any, Any] = models.IntegerField(default=0)

    # reveal_type(votes)  # -> django.db.models.fields.IntegerField[Any, Any]

    def vote(self) -> None:
        # reveal_type(self)  # -> polls.models.Choice
        self.votes = F('votes') + 1
        self.save(update_fields=['votes'])

    def __str__(self) -> str:
        # reveal_type(self)  # -> polls.models.Choice
        # reveal_type(self.choice_text)  # -> Any
        return str(self.choice_text)
