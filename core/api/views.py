from django.contrib.auth import login
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Account
from dashboard.models import Product, Service, Transaction, Wallet

from .serializers import (AccountSerializer, ProductSerializer,
                          RegisterSerializer, ServiceSerializer,
                          TransactionSerializer, UserSerializer,
                          WalletSerializer)


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


class AccountList(APIView):

    def get(self, request):
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)


class AccountDetail(APIView):

    def get(self, request, pk, *args, **kwargs):
        account = Account.objects.filter(id=pk).first()
        serializer = AccountSerializer(account, many=False)
        return Response(serializer.data)


class ProductList(APIView):

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetail(APIView):

    def get(self, request, pk, *args, **kwargs):
        product = Product.objects.filter(id=pk).first()
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)


class ServiceList(APIView):

    def get(self, request):
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)


class ServiceDetail(APIView):

    def get(self, request, pk, *args, **kwargs):
        service = Service.objects.filter(id=pk).first()
        serializer = ServiceSerializer(service, many=False)
        return Response(serializer.data)


class TransactionList(APIView):

    def get(self, request):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)


class TransactionDetail(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, pk, *args, **kwargs):
        transaction = Transaction.objects.filter(id=pk).first()
        serializer = TransactionSerializer(transaction, many=False)
        return Response(serializer.data)


class WalletList(APIView):

    def get(self, request):
        wallets = Wallet.objects.all()
        serializer = WalletSerializer(wallets, many=True)
        return Response(serializer.data)


class WalletDetail(APIView):

    def get(self, request, pk, *args, **kwargs):
        wallet = Wallet.objects.filter(id=pk).first()
        serializer = WalletSerializer(wallet, many=False)
        return Response(serializer.data)


class RegisterAPI(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)
