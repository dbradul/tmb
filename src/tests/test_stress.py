import requests

from django.core.management import call_command
from django.urls import reverse
from django.test import TestCase
from django.test import Client

from testsuite.models import Test, TestResult

PK = 1

URL_BASE = 'http://ec2-100-25-166-94.compute-1.amazonaws.com'
TOKEN = ''
#
class BaseFlowTest(TestCase):

    def setUp(self):
        call_command('loaddata', 'tests/fixtures/accounts.json', verbosity=0)
        call_command('loaddata', 'tests/fixtures/tests.json', verbosity=0)
        self.client = Client()
        self.client.login(username='admin', password='admin')

    def _authenticate(self):
        url = f"{URL_BASE}{reverse('login')}"
        response = requests.post(url, {'username': 'Admin', 'password': 'admin'})
        self.assertEqual(200, response.status_code)


    def test_stress(self):
        COOKIES = {
            'sessionid': 'v4px90h0rkkncm5ksnr0vzpe2lr4an1f',
            'csrftoken': 'Ka43DM1c8be87cdmvGD15oUVJg180N1NrXazGPVAgsJRDTvjJzQvVvrA81U58KRK'
        }
        # self._authenticate()
        url = f"{URL_BASE}{reverse('test:start', kwargs={'pk': PK})}"
        response = requests.get(
            url=url,
            # cookies=COOKIES
        )
        self.assertEqual(200, response.status_code)
        # self.client.get(reverse('test:start', kwargs={'pk': PK}))

        test = Test.objects.get(pk=PK)
        questions = test.questions.all()
        url = f"{URL_BASE}{reverse('test:next', kwargs={'pk': PK})}"

        for idx, question in enumerate(questions, 1):
            requests.get(url)#, cookies=COOKIES)
            correct_answers = {
                f'answer_{idx}' : '1'
                for idx, answer in enumerate(question.answers.all(), 1)
                if answer.is_correct
            }
            response = requests.post(
                url=url,
                data=correct_answers,
                # cookies=COOKIES
            )
            self.assertEqual(200, response.status_code)

        # test_result = TestResult.objects.order_by('-id').first()
        self.assertEqual(200, response.status_code)#test.questions_count(), test_result.avr_score)
