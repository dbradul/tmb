from django.urls import reverse
from django.test import TestCase
from django.test import Client

from account.models import User

CREDENTIALS = {
    'username': 'AdminUser',
    'first_name': 'AdminUserFirst',
    'last_name': 'AdminUserLast',
    'email': 'email@admin.com',
    'password1': 'FhTy123@#$%',
    'password2': 'FhTy123@#$%',
}


class RegistrationTests(TestCase):

    def setUp(self):
        self.client = Client()

    def _register(self, credentials):
        url = reverse('registration')
        return self.client.post(url, credentials)

    def test_registration(self):
        users_count = User.objects.count()
        response = self._register(CREDENTIALS)
        assert response.url.startswith(reverse('login'))
        assert response.status_code == 302
        assert User.objects.count() == (users_count + 1)

    def test_login(self):
        self._register(CREDENTIALS)
        self.client.login(username='AdminUser', password='FhTy123@#$%')
        response = self.client.get(reverse('profile'))
        assert response.status_code == 200
        assert 'Update' in response.content.decode()


