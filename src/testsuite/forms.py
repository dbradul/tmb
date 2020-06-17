from django.core.exceptions import ValidationError
from django.forms import ModelForm, BaseInlineFormSet

from testsuite.models import Question, TestSuite


class QuestionEditForm(ModelForm):
    model = Question

    def clean(self):
        pass


class VariantInlineFormset(BaseInlineFormSet):

    def clean(self):
        variants = [
            form.cleaned_data.get('correct', False)
            for form in self.forms
        ]

        if not (self.instance.MIN_LIMIT <= len(variants) <= self.instance.MAX_LIMIT):
            raise ValidationError(f'Number of variants is out of range [{self.instance.MIN_LIMIT}..{self.instance.MAX_LIMIT}]')

        if all(variants):
            raise ValidationError('It is prohibited to set *ALL* variant as correct!')

        if not any(variants):
            raise ValidationError('It is prohibited to *NOT SET* at least one variant as correct!')


class TestSuiteEditForm(ModelForm):
    model = TestSuite

    def clean(self):
        pass