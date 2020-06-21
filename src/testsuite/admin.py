from django.contrib import admin

# Register your models here.
from django.core.exceptions import ValidationError

from testsuite.forms import QuestionForm, VariantInlineFormset
from testsuite.models import Test, Question, Answer, TestRun


class AnswersInline(admin.TabularInline):
    model = Answer
    fields = ('text', 'is_correct')
    show_change_link = False
    extra = 0
    formset = VariantInlineFormset


class QuestionAdminModel(admin.ModelAdmin):
    list_display = ('number', 'text', 'description', 'test')
    list_select_related = ('test',)
    list_per_page = 10
    search_fields = ('first_name',)
    inlines = (AnswersInline,)
    form = QuestionForm


class QuestionsInline(admin.TabularInline):
    model = Question
    fields = ('text', )
    show_change_link = True
    extra = 1


class TestAdminModel(admin.ModelAdmin):
    fields = ('title', 'description', 'level', 'image')
    list_display = ('title', 'description', 'level', 'image')
    list_per_page = 10
    inlines = (QuestionsInline,)


admin.site.register(Test, TestAdminModel)
admin.site.register(Question, QuestionAdminModel)
admin.site.register(Answer)
admin.site.register(TestRun)
