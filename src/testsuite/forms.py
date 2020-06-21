from django.core.exceptions import ValidationError
from django.forms import ModelForm, BaseInlineFormSet, Form, forms, fields
from django.forms import widgets

from testsuite.models import Question, Test




class TestRunForm(Form):
    # model = Question
    answer_variant = fields.CharField(label='Answer variant', required=False)
    answer_selection = fields.BooleanField(label='Answer selection', initial=False, required=False)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['description'].disabled = True
    #     self.fields['text'].disabled = True
    #     self.fields['number'].disabled = True
        # self.fields['description'].widget.attrs['readonly'] = True

    def clean(self):
        pass


class QuestionForm(ModelForm):
    model = Question

    class Meta:
        fields = ['description', 'text', 'number']#'__all__'
        # exclude =
        widgets = {'description': widgets.Textarea(
            attrs={'placeholder': 'Please enter your text...'}
        )}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].disabled = True
        self.fields['text'].disabled = True
        self.fields['number'].disabled = True
        # self.fields['description'].widget.attrs['readonly'] = True

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