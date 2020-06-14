from django.contrib import admin

# Register your models here.
from testsuite.forms import QuestionEditForm
from testsuite.models import TestSuite, Question, Variant, TestSuiteRun


class VariantsInline(admin.TabularInline):
    model = Variant
    fields = ('text', 'correct')
    show_change_link = True


class QuestionAdminModel(admin.ModelAdmin):
    list_display = ('text', 'description', 'test_suite')
    list_select_related = ('test_suite',)
    # readonly_fields = ('num_variant_min_limit', )
    list_per_page = 10
    search_fields = ('first_name',)
    inlines = (VariantsInline,)
    form = QuestionEditForm

    def save_form(self, request, form, change):
        return super().save_form(request, form, change)

    def num_variant_min_limit(self, instance):
        return instance.num_variant_min_limit


class QuestionsInline(admin.TabularInline):
    model = Question
    fields = ('text', ) #'num_variant_min_limit')
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


#
# class StudentsInline(admin.TabularInline):
#     model = Student
#     readonly_fields = ('birthdate', 'last_name', 'first_name', 'email')
#     show_change_link = True
#
#
# class GroupAdmin(admin.ModelAdmin):
#     fields = ['name', 'classroom']
#     inlines = (StudentsInline,)
#     list_per_page = 10
#
# admin.site.register(Group, GroupAdmin)