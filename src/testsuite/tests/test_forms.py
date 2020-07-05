import datetime

from django.core.management import call_command
from django.test import TestCase
from django.test import Client

from testsuite.forms import QuestionForm, AnswerInlineFormset
from testsuite.models import Test, Question


class QuestionFormTests(TestCase):

    def setUp(self):
        self.client = Client()
        test = Test.objects.create(title='Test test')
        Question.objects.create(
            test=test,
            number=1,
            text='Some text'
        )

    def test_valid(self):
        test = Test.objects.first()
        form_data = {
            'title': 'Title',
            'number': 1,
            'text': 'Text',
            'test': test
        }
        form = QuestionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid(self):
        test = Test.objects.first()
        form_data = {
            'title': 'Title',
            # 'number': 1,
            'text': 'Text',
            'test': test
        }
        form = QuestionForm(data=form_data)
        self.assertFalse(form.is_valid())

