import datetime

from django.core.management import call_command
from django.test import TestCase
from django.test import Client
from django.urls import reverse

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

    def _run_test(self, test):
        self.client.get(reverse('test:start', kwargs={'pk': test.id}))
        next_url = reverse('test:next', kwargs={'pk': test.id})
        for step in range(1, test.questions_count()+1):
            self.client.get(next_url)
            self.client.post(
                path=next_url,
                data={
                    'answer_1': "1"
                }
            )

    def setUp(self):
        call_command('loaddata', 'tests/fixtures/accounts.json', verbosity=0)
        call_command('loaddata', 'tests/fixtures/tests_min.json', verbosity=0)
        self.client = Client()
        self.client.login(username='admin', password='admin')

    def test_last_run(self):
        test = Test.objects.first()
        utc_now = datetime.datetime.now(tz=datetime.timezone.utc)

        prev_last_run = test.last_run()
        self._run_test(test)
        new_last_run = test.last_run()

        self.assertLess(prev_last_run, new_last_run)
        self.assertLess(utc_now, new_last_run)
