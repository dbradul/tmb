from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.test import TestCase
from django.test import Client


class UrlsAvailabilityTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_public_url(self):
        response = self.client.get(reverse('registration'))
        assert response.status_code == 200
        assert 'Register' in response.content.decode()

        response = self.client.get(reverse('login'))
        assert response.status_code == 200
        assert 'Login' in response.content.decode()

    def test_private_urls(self):
        response = self.client.get(reverse('profile'))
        assert response.url.startswith(reverse('login'))
        assert response.status_code == 302

        response = self.client.get(reverse('logout'))
        assert response.url.startswith(reverse('login'))
        assert response.status_code == 302
