from django.core.exceptions import ValidationError
from django.forms import ModelForm, BaseInlineFormSet

from testsuite.models import Question, Test



class TestForm(ModelForm):

    class Meta:
        model = Test
        fields = '__all__'

    def clean(self):
        pass


class QuestionForm(ModelForm):

    class Meta:
        model = Question
        fields = '__all__'


    def clean(self):
        pass


class QuestionsInlineForm(ModelForm):

    def clean(self):
        pass


class QuestionsInlineFormSet(BaseInlineFormSet):

    def clean(self):
        if not (self.instance.MIN_LIMIT <= len(self.forms) <= self.instance.MAX_LIMIT):
            raise ValidationError('Quantity of question is out of range ({}..{})'.format(
                self.instance.MIN_LIMIT, self.instance.MAX_LIMIT
            ))


class AnswerInlineFormset(BaseInlineFormSet):
    def clean(self):
        if not (self.instance.MIN_LIMIT <= len(self.forms) <= self.instance.MAX_LIMIT):
            raise ValidationError('Quantity of answers is out of range ({}..{})'.format(
                self.instance.MIN_LIMIT, self.instance.MAX_LIMIT
            ))

        correct_list = [
            form.cleaned_data['is_correct']
            for form in self.forms
        ]

        if not any(correct_list):
            raise ValidationError('You should select AT LEAST one correct answer!')

        if all(correct_list):
            raise ValidationError('You should NOT select ALL correct answers!')
