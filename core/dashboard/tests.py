from django.test import TestCase
from http import HTTPStatus
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

    def test_singup_page_renders(self):
        url = reverse("accounts:sign_up")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertIn("Sign Up".encode(), resp.content)

    def test_user_sign_up_failed(self):
        url = reverse("accounts:sign_up")
        data = {
            "username": self.TEST_USERNAME,
            "fullname": self.TEST_FULLANME,
            "password": self.TEST_PASSWORD,
            "email": self.TEST_EMAIL,
            "confirm_password": "wrong-pass",
        }
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, HTTPStatus.FOUND)
        self.assertEqual(resp["Location"], reverse("accounts:sign_up"))

    def test_user_sign_up_success(self):
        url = reverse("accounts:sign_up")
        data = {
            "username": self.TEST_USERNAME,
            "fullname": self.TEST_FULLANME,
            "password": self.TEST_PASSWORD,
            "email": self.TEST_EMAIL,
            "confirm_password": self.TEST_PASSWORD,
        }
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, HTTPStatus.FOUND)
        self.assertNotEqual(resp["Location"], reverse("accounts:sign_up"))

    def test_user_login_success(self):
        # Sign up
        self.test_user_sign_up_success()
        url = reverse("accounts:login")
        data = {
            "username": self.TEST_USERNAME,
            "password": self.TEST_PASSWORD,
        }
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, HTTPStatus.FOUND)
        self.assertNotEqual(resp["Location"], reverse("accounts:login"))
        self.assertNotEqual(resp["Location"], reverse("accounts:sign_up"))

    def test_user_login_failed(self):
        # Sign up
        self.test_user_sign_up_success()
        url = reverse("accounts:login")
        data = {
            "username": self.TEST_USERNAME,
            "password": "wrong-pass",
        }
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertIn("Invalid credentials".encode(), resp.content)


class TestLogoutView(TestCase):
    def test_logout_page_renders(self):
        url = reverse('accounts:logout')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('accounts:login'))
