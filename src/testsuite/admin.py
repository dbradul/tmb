from django.contrib import admin

# Register your models here.
from django.core.exceptions import ValidationError

from testsuite.forms import QuestionEditForm, VariantInlineFormset
from testsuite.models import TestSuite, Question, Variant, TestSuiteRun


class VariantsInline(admin.TabularInline):
    model = Variant
    fields = ('text', 'correct')
    show_change_link = False
    extra = 0
    formset = VariantInlineFormset


class QuestionAdminModel(admin.ModelAdmin):
    list_display = ('text', 'description', 'test_suite')
    list_select_related = ('test_suite',)
    # readonly_fields = ('num_variant_min_limit', )
    list_per_page = 10
    search_fields = ('first_name',)
    inlines = (VariantsInline,)
    form = QuestionEditForm


    # def save_form(self, request, form, change):
    #     return super().save_form(request, form, change)
    #
    # def save_model(self, request, obj, form, change):
    #     return super().save_model(request, obj, form, change)
    #
    # def save_formset(self, request, form, formset, change):
    #     variants = []
    #     for f in formset:
    #         if f.is_valid():
    #             instance = f.save(commit=False)
    #             variants.append(instance)
    #         else:
    #             for err in f.errors:
    #                 f.add_error(None, err)
    #             # raise f.ValidationError(f.errors)
    #
    #     if all([v.correct for v in variants]):
    #         # raise formset.ValidationError('It is prohibited to set all variant as correct!')
    #         form.add_error(None, ValidationError('It is prohibited to set all variant as correct!'))
    #     if not any([v.correct for v in variants]):
    #         # raise formset.ValidationError('It is prohibited to not set at least variant as correct!')
    #         form.add_error(None, ValidationError('It is prohibited to not set at least variant as correct!'))
    #
    #     if not form.errors:
    #         return super().save_formset(request, form, formset, change)
    #
    #
    # def save_related(self, request, form, formsets, change):
    #     return super().save_related(request, form, formsets, change)


class QuestionsInline(admin.TabularInline):
    model = Question
    fields = ('text', )#'num_variant_min_limit')
    show_change_link = True
    extra = 1

# class StudentAdmin(admin.ModelAdmin):
#     list_display = ('first_name', 'last_name', 'email', 'group')
#     list_select_related = ('group',)
#     list_per_page = 10
#     search_fields = ('first_name',)


class TestSuiteAdminModel(admin.ModelAdmin):
    fields = ('title', 'description', 'level', 'image')
    list_display = ('title', 'description', 'level', 'image')
    list_per_page = 10
    inlines = (QuestionsInline,)


admin.site.register(TestSuite, TestSuiteAdminModel)
admin.site.register(Question, QuestionAdminModel)
admin.site.register(Variant)
admin.site.register(TestSuiteRun)
