import imp
from django.shortcuts import render
from django.views import View
from accounts.models import Account
from dashboard.models import Product, Service, Transaction, Wallet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.decorators import method_decorator


from .serializers import AccountSerializer, WalletSerializer, TransactionSerializer, ProductSerializer, ServiceSerializer


class APIOverView(View):

    @method_decorator(api_view(['GET']))
    def get(self, request):
        api_urls = {
            'Login': '/api/login/',
            'Logout': '/api/logout/',
            'User': '/api/user/',
            'UserList': '/api/user-list/',
            'UserDetail': '/api/user-detail/<str:pk>/',
            'UserCreate': '/api/user-create/',
            'UserUpdate': '/api/user-update/<str:pk>/',
            'UserDelete': '/api/user-delete/<str:pk>/',
            'UserPassword': '/api/user-password/<str:pk>/',
        }
        return Response(api_urls)


class AccountList(View):

    @method_decorator(api_view(['GET']))
    def get(self, request):
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)


class ProductList(View):

    @method_decorator(api_view(['GET']))
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ServiceList(View):

    @method_decorator(api_view(['GET']))
    def get(self, request):
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)


class TransactionList(View):

    @method_decorator(api_view(['GET']))
    def get(self, request):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)


class WalletList(View):

    @method_decorator(api_view(['GET']))
    def get(self, request):
        wallets = Wallet.objects.all()
        serializer = WalletSerializer(wallets, many=True)
        return Response(serializer.data)


class OneUser(View):

    @method_decorator(api_view(['GET']))
    def get(self, request, pk):
        user = Account.objects.filter(id=pk).first()
        serializer = AccountSerializer(user)
        return Response(serializer.data)


class SignUp(View):

    @method_decorator(api_view(['POST']))
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
