from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.test import TestCase
from django.test import Client


class UrlsAvailabilityTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_public_url(self):
        response = self.client.get(reverse('index'))
        assert response.status_code == 200
        assert 'Welcome to TMB!' in response.content.decode()

        response = self.client.get(reverse('test:list'))
        assert response.status_code == 200
        assert 'Test list' in response.content.decode()

        # response = self.client.get(reverse('test:start', kwargs={'pk': 1}))
        # assert response.status_code == 200

        # response = self.client.get(reverse('test:next'))
        # assert response.status_code == 200

    def test_private_urls(self):
        response = self.client.get(reverse('leaderboard'))
        assert response.url.startswith(reverse('login'))
        assert response.status_code == 302
