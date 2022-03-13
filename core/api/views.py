import imp
from multiprocessing import Manager
from django.shortcuts import render
from django.views import View
from accounts.models import Account
from dashboard.models import Product, Service, Transaction, Wallet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.decorators import method_decorator


from .serializers import AccountSerializer, WalletSerializer, TransactionSerializer, ProductSerializer, ServiceSerializer, SignUpSerializer


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


class AccountDetail(View):

    @method_decorator(api_view(['GET']))
    def get(self, request, pk, *args, **kwargs):
        account = Account.objects.filter(id=pk).first()
        serializer = AccountSerializer(account, many=False)
        return Response(serializer.data)


class ProductList(View):

    @method_decorator(api_view(['GET']))
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetail(View):

    @method_decorator(api_view(['GET']))
    def get(self, request, pk, *args, **kwargs):
        product = Product.objects.filter(id=pk).first()
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)


class ServiceList(View):

    @method_decorator(api_view(['GET']))
    def get(self, request):
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)


class ServiceDetail(View):

    @method_decorator(api_view(['GET']))
    def get(self, request, pk, *args, **kwargs):
        service = Service.objects.filter(id=pk).first()
        serializer = ServiceSerializer(service, many=False)
        return Response(serializer.data)


class TransactionList(View):

    @method_decorator(api_view(['GET']))
    def get(self, request):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)


class TransactionDetail(View):

    @method_decorator(api_view(['GET']))
    def get(self, request, pk, *args, **kwargs):
        transaction = Transaction.objects.filter(id=pk).first()
        serializer = TransactionSerializer(transaction, many=False)
        return Response(serializer.data)


class WalletList(View):

    @method_decorator(api_view(['GET']))
    def get(self, request):
        wallets = Wallet.objects.all()
        serializer = WalletSerializer(wallets, many=True)
        return Response(serializer.data)


class WalletDetail(View):

    @method_decorator(api_view())
    def get(self, request, pk, *args, **kwargs):
        wallet = Wallet.objects.filter(id=pk).first()
        serializer = WalletSerializer(wallet, many=False)
        return Response(serializer.data)


class SignUp(View):

    @method_decorator(api_view(['GET', 'POST']))
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
