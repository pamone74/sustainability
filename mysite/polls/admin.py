from django.contrib import admin
# Register your models here.
from .models import  Choice, Question
# admin.site.register(Question)
# admin.site.register(Choice)
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    # fieldsets = [
        # # (None, {"fields": ["question_text"]}), ("Date information", {"fields": ["pub_date"], "classes":["collapse"]}),
    # ]
    # inlines = [ChoiceInline]
    list_display  = ["question_text", "pub_date", "was_published"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]

admin.site.register(Question, QuestionAdmin)

