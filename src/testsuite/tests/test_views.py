from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.core.management import call_command
from django.urls import reverse
from django.test import TestCase
from django.test import Client

from testsuite.models import Test, TestResult

PK = 1

class BaseFlowTest(TestCase):

    def setUp(self):
        call_command('loaddata', 'tests/fixtures/accounts.json', verbosity=0)
        call_command('loaddata', 'tests/fixtures/tests.json', verbosity=0)
        self.client = Client()
        self.client.login(username='admin', password='admin')


    def test_basic_flow(self):
        response = self.client.get(reverse('test:start', kwargs={'pk': PK}))
        assert response.status_code == 200
        assert 'START ▶' in response.content.decode()

        test = Test.objects.get(pk=PK)
        questions_count = test.questions_count()
        url = reverse('test:next', kwargs={'pk': PK})

        for step in range(1, questions_count+1):
            response = self.client.get(url)
            assert response.status_code == 200
            assert 'Submit' in response.content.decode()
            response = self.client.post(
                path=url,
                data={
                    'answer_1': "1"
                }
            )
            if step < questions_count:
                self.assertRedirects(response, url)
            else:
                assert response.status_code == 200

        assert 'START ANOTHER TEST ▶' in response.content.decode()


    def test_success_flow(self):
        self.client.get(reverse('test:start', kwargs={'pk': PK}))

        test = Test.objects.get(pk=PK)
        questions = test.questions.all()
        url = reverse('test:next', kwargs={'pk': PK})

        for idx, question in enumerate(questions, 1):
            self.client.get(url)
            correct_answers = {
                f'answer_{idx}' : '1'
                for idx, answer in enumerate(question.answers.all(), 1)
                if answer.is_correct
            }
            self.client.post(
                path=url,
                data=correct_answers
            )

        test_result = TestResult.objects.order_by('-id').first()
        self.assertEqual(test.questions_count(), test_result.avr_score)
