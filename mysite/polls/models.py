import datetime
from django.db import models
import datetime
from django.utils import timezone
from django.contrib import admin
from django.utils.translation import gettext as _

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date Published")
    @admin.display(
            boolean=True,
            ordering="pub_date",
            description="published recently?",
    )
    def was_published(self):
        now  = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    def __str__(self):
        return self.question_text
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def choice_validate(self):
        return self.choice_text
    def __str__(self):
        return self.choice_text

class Bookd(models.Model):
    title = models.CharField(_(""), max_length=50)

    def create(cls,title):
        book = cls(title=title)
        book = book + "amone Patrik"
        return book
book=Bookd.create("pride and prejuice")