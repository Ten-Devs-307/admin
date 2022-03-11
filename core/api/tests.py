from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus


class TestAPIOverview(TestCase):

    def test_api_overview_returns(self):
        url = reverse('api:api_overview')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)


class TestAccountList(TestCase):

    def test_account_list_returns(self):
        url = reverse('api:account_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)


class TestProductList(TestCase):

    def test_product_list_returns(self):
        url = reverse('api:product_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)


class TestServiceList(TestCase):

    def test_service_list_returns(self):
        url = reverse('api:service_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)


class TestTransactionList(TestCase):

    def test_transaction_list_returns(self):
        url = reverse('api:transaction_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
