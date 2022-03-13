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
