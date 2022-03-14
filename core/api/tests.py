from urllib import response
from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus


class TestAPIOverview(TestCase):

    def test_api_overview_returns(self):
        url = reverse('api:api_overview')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)


class TestAccount(TestCase):

    def test_account_list_returns(self):
        url = reverse('api:account_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_account_detail_returns(self):
        url = reverse('api:user', args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)


class TestProduct(TestCase):

    def test_product_list_returns(self):
        url = reverse('api:product_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_product_detail_returns(self):
        url = reverse('api:product', args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)


class TestService(TestCase):

    def test_service_list_returns(self):
        url = reverse('api:service_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_service_detail_returns(self):
        url = reverse('api:service', args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)


class TestTransaction(TestCase):

    def test_transaction_list_returns(self):
        url = reverse('api:transaction_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_transaction_detail_returns(self):
        url = reverse('api:transaction', args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)


class TestWallet(TestCase):

    def test_wallet_list_returns(self):
        url = reverse('api:wallet_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_wallet_detail_returns(self):
        url = reverse('api:wallet', args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)


class TestSignUP(TestCase):

    def test_signup_returns_for_get(self):
        url = reverse('api:sign_up')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_signup_returns_for_post(self):
        url = reverse('api:sign_up')
        data = {"name": "test", "email": "test@gmail.com", "password": "test"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def test_signup_no_password(self):
        url = reverse('api:sign_up')
        data = {"name": "test", "email": "test@gmail.com"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, HTTPStatus.PARTIAL_CONTENT)

    def test_signup_no_email(self):
        url = reverse('api:sign_up')
        data = {"name": "test", "password": "password"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, HTTPStatus.PARTIAL_CONTENT)
