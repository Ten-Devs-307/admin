from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class TestDashboard(TestCase):
    def test_dashboard_view(self):
        url = reverse('dashboard:dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)


class TestLoginView(TestCase):
    TEST_PASSWORD = "PASS"
    TEST_USERNAME = "NAME"
    TEST_FULLANME = "FULL NAME"
    TEST_EMAIL = "testemail@payhub.com"

    def test_login_page_renders(self):
        url = reverse("accounts:login")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertIn("Login".encode(), resp.content)


class TestLogoutView(TestCase):
    def test_logout_page_renders(self):
        url = reverse('accounts:logout')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('accounts:login'))
