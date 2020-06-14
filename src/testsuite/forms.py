from django.core.exceptions import ValidationError
from django.forms import ModelForm

from testsuite.models import Question


class QuestionEditForm(ModelForm):
    model = Question

    def clean(self):
        variants = self.instance.variants.all()
        if all([v.correct for v in variants]):
            raise ValidationError('It is prohibited to set all variant as correct!')
        if not any([v.correct for v in variants]):
            raise ValidationError('It is prohibited to not set at least variant as correct!')