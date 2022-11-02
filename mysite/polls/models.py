from datetime import datetime, timedelta
from django.utils import timezone
from django.db import models
from django.db.models import F
from django.contrib import admin
from traitlets import Bool
# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=512)
    pub_date = models.DateTimeField("date_published")

    def __str__(self) -> str:
        return self.question_text

    @admin.display(boolean=True,
                   ordering='pub_date',
                   description='Published recently')
    def was_published_recently(self) -> bool:
        now = timezone.now()
        return (
            self.pub_date >= timezone.now() - timedelta(days=1)
            and self.pub_date <= now
        )


class Choice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="choice_set"
    )
    choice_text = models.CharField(max_length=512)
    votes = models.IntegerField(default=0)

    def vote(self) -> None:
        self.votes = F('votes') + 1
        self.save(update_fields=['votes'])

    def __str__(self) -> str:
        return self.choice_text
