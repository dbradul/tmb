import datetime

from django.core.management import call_command
from django.test import TestCase
from django.test import Client

from testsuite.models import Test, Question


class TestModelBaseTests(TestCase):

    def setUp(self):
        self.client = Client()
        test = Test.objects.create(title='Test test')
        Question.objects.create(
            test=test,
            number=1,
            text='Some text'
        )

    def test_question_count(self):
        test = Test.objects.first()
        self.assertEqual(1, test.questions_count())

    def test_str(self):
        test = Test.objects.first()
        self.assertEqual('Test test', str(test))

    def test_last_run(self):
        test = Test.objects.first()
        self.assertEqual('', test.last_run())


class TestModelExtendedTests(TestCase):

    def setUp(self):
        call_command('loaddata', 'tests/fixtures/accounts.json', verbosity=0)
        call_command('loaddata', 'tests/fixtures/tests_min.json', verbosity=0)
        self.client = Client()
        self.client.login(username='admin', password='admin')
    #
    # def test_question_count(self):
    #     test = Test.objects.first()
    #     self.assertEqual(4, test.questions_count())

    def test_last_run(self):
        test = Test.objects.first()
        dt = datetime.datetime.strptime('2020-06-28T17:59:33.970Z', "%Y-%m-%dT%H:%M:%S.%f%z")
        self.assertEqual(dt, test.last_run())

