from django.core.exceptions import ValidationError
from django.forms import ModelForm, BaseInlineFormSet, Form, forms, fields
from django.forms import widgets

from testsuite.models import Question, Test


class QuestionForm(ModelForm):
    model = Question

    class Meta:
        fields = '__all__'

    def clean(self):
        pass


class VariantInlineFormset(BaseInlineFormSet):

    def clean(self):
        variants = [
            form.cleaned_data.get('is_correct', False)
            for form in self.forms
        ]

        if not (self.instance.MIN_LIMIT <= len(variants) <= self.instance.MAX_LIMIT):
            raise ValidationError(f'Number of variants is out of range [{self.instance.MIN_LIMIT}..{self.instance.MAX_LIMIT}]')

        if all(variants):
            raise ValidationError('It is prohibited to set *ALL* variant as correct!')

        if not any(variants):
            raise ValidationError('It is prohibited to *NOT SET* at least one variant as correct!')


class TestSuiteEditForm(ModelForm):
    model = Test

    def clean(self):
        pass