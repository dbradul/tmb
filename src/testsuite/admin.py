from django.contrib import admin

from testsuite.forms import (
    TestForm,
    QuestionsInlineFormSet,
    QuestionsInlineForm,
    AnswerInlineFormset
)
from testsuite.models import Test, Question, Answer, TestRun


class AnswersInline(admin.TabularInline):
    model = Answer
    fields = ('text', 'is_correct')
    show_change_link = False
    extra = 0
    formset = AnswerInlineFormset


class QuestionAdminModel(admin.ModelAdmin):
    list_display = ('number', 'text', 'description', 'test')
    list_select_related = ('test',)
    list_per_page = 10
    search_fields = ('first_name',)
    inlines = (AnswersInline,)
    # form = QuestionForm


class QuestionsInline(admin.TabularInline):
    model = Question
    fields = ('text', 'number')
    show_change_link = True
    extra = 0
    form = QuestionsInlineForm
    formset = QuestionsInlineFormSet


class TestAdminModel(admin.ModelAdmin):
    fields = ('title', 'description', 'level', 'image')
    list_display = ('title', 'description', 'level', 'image')
    list_per_page = 10
    inlines = (QuestionsInline,)
    form = TestForm


admin.site.register(Test, TestAdminModel)
admin.site.register(Question, QuestionAdminModel)
admin.site.register(Answer)
admin.site.register(TestRun)
