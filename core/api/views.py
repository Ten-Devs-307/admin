import time
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.views import View
from core import settings
from core.util.util_functions import get_transaction_status, receive_payment
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from accounts.models import Account
from dashboard.models import JobCategory, Product, Service, Transaction, Wallet

from core.util.constants import Status as S
from .serializers import (AccountSerializer, PaymentSerializer, ProductSerializer,
                          RegisterSerializer, JobSerializer,
                          TransactionSerializer, UserSerializer,
                          WalletSerializer, JobCategorySerializer)


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


class JobsList(APIView):
    def get(self, request, *args, **kwargs):
        services = Service.objects.all().order_by('-id')
        serializer = JobSerializer(services, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        '''Use the post method to save upload data'''
        '''Get token from request, substring token to get token key, use token key to get user'''
        token_str = request.META.get('HTTP_AUTHORIZATION').split(' ')[1][0:8]
        customer = AuthToken.objects.filter(
            token_key=token_str).first().user
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=customer)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AcceptDeclineJob(APIView):
    '''For labourer to accept or decline job'''

    def post(self, request, pk, *args, **kwargs):
        job = Service.objects.filter(id=pk).first()
        job_status = True if request.data.get(
            'status') == S.ACCEPTED.value else False

        job.accepted = job_status
        if job_status:
            '''Check if user used token authentication'''
            try:
                token_str = request.META.get(
                    'HTTP_AUTHORIZATION').split(' ')[1][0:8]
            except AttributeError:
                return Response({"status": "error", "data": "Token not found"}, status=status.HTTP_400_BAD_REQUEST)
            labourer = AuthToken.objects.filter(
                token_key=token_str).first().user
            job.labourer = labourer
            job.save()
            return Response({"status": "success", "data": JobSerializer(job, many=False).data})
        else:
            '''If job is declined, set labourer to null'''
            job.labourer = None
            job.save()
            return Response({"status": "success", "data": JobSerializer(job, many=False).data})


class CancelJob(APIView):
    '''For customer to cancel job'''

    def post(self, request, pk, *args, **kwargs):
        token_str = request.META.get('HTTP_AUTHORIZATION').split(' ')[1][0:8]
        customer = AuthToken.objects.filter(
            token_key=token_str).first().user
        job = Service.objects.filter(id=pk, customer=customer).first()
        '''Only allow cancellation of jobs when it hasnt been accepted by any labourer'''
        if job.accepted and job.labourer:
            return Response({"status": "failed", "reason": "Job is already accepted by labourer"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            job.status = S.CANCELLED.value
            job.save()
            return Response({"status": "success", "reason": "Job Cancelled Successfully"})


class CompleteJobAPI(APIView):
    '''For labourer to mark job as completed'''

    def post(self, request, pk, *args, **kwargs):
        token_str = request.META.get('HTTP_AUTHORIZATION').split(' ')[1][0:8]
        labourer = AuthToken.objects.filter(
            token_key=token_str).first().user
        job = Service.objects.filter(
            id=pk, labourer=labourer, accepted=True).first()
        job_status = request.data.get('status')
        if job:
            if job_status == S.COMPLETED.value:
                job.status = S.COMPLETED.value
                job.save()
                return Response({"status": "success", "reason": "Job Completed Successfully"})
            else:
                return Response({"status": "failed", "reason": "Something went wrong, Couldn't complete job."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status": "failed", "reason": "Job not found."}, status=status.HTTP_400_BAD_REQUEST)


class ConfirmJobCompletionAPI(APIView):
    '''For customer to confirm that labourer has completed the job'''

    def post(self, request, pk, *args, **kwargs):
        token_str = request.META.get('HTTP_AUTHORIZATION').split(' ')[1][0:8]
        customer = AuthToken.objects.filter(
            token_key=token_str).first().user
        job = Service.objects.filter(
            id=pk, customer=customer, accepted=True).first()
        job_status = True if request.data.get(
            'status') == S.CONFIRMED.value else False
        if job:
            if job_status:
                job.completion_confirmed = job_status
                job.save()
                return Response({"status": "success", "reason": "Job Completion Confirmed Successfully"})
            return Response({"status": "error", "reason": "Job Completion Not Confirmed"})
        else:
            return Response({"status": "failed", "reason": "Job not found."}, status=status.HTTP_400_BAD_REQUEST)


class JobDetail(APIView):

    def get(self, request, pk, *args, **kwargs):
        service = Service.objects.filter(id=pk).first()
        serializer = JobSerializer(service, many=False)
        return Response(serializer.data)


class TransactionList(APIView):

    def get(self, request):
        transactions = Transaction.objects.all().order_by('-id')
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
        wallets = Wallet.objects.all().order_by('-id')
        serializer = WalletSerializer(wallets, many=True)
        return Response(serializer.data)


class WalletDetail(APIView):

    def get(self, request, pk, *args, **kwargs):
        wallet = Wallet.objects.filter(id=pk).first()
        serializer = WalletSerializer(wallet, many=False)
        return Response(serializer.data)


class JobCategoryAPI(APIView):
    def get(self, request, *args, **kwargs):
        categories = JobCategory.objects.filter(published=True).order_by('-id')
        serializer = JobCategorySerializer(categories, many=True)
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


class MakePaymentAPI(APIView):
    def generate_transaction_id(self):
        return int(round(time.time() * 1000))

    def post(self, request, pk, *args, **kwargs):  # pk is for job
        token_str = request.META.get('HTTP_AUTHORIZATION').split(' ')[1][0:8]
        customer = AuthToken.objects.filter(
            token_key=token_str).first().user
        wallet = Wallet.objects.filter(holder=customer).first()
        serializer = PaymentSerializer(data=request.data)
        # get job in question
        job = Service.objects.filter(id=pk).first()

        if serializer.is_valid():
            serializer.save(customer=customer, job=job)
            transaction_id = self.generate_transaction_id()
            data = {
                'transaction_id': transaction_id,
                'mobile_number': serializer['from_phone'].value,
                'amount': serializer['amount'].value,
                'wallet_id': settings.WALLET_ID,
                'network_code': serializer['network'].value,
                'note': 'Cashout',
            }
            # initiate payment
            receive_payment(data)

            for i in range(4):
                time.sleep(5)
                transaction_status = get_transaction_status(
                    transaction_id)
                if transaction_status['success'] == True:
                    print('the transaction was successful')
                    break

            transaction = {
                'transaction_id': transaction_id,
                'amount': serializer['amount'].value,
                'from_phone': serializer['from_phone'].value,
                'network': serializer['network'].value,
                'note': 'Payment',
                'payment_status_code': transaction_status['status_code'],
                'payment_status': transaction_status['message'],
                'customer': customer,
                'job': job,
                'service': job.service_name,
                'wallet': wallet,
            }
            print("Saving Transaction")
            Transaction.objects.create(**transaction)
            print('Transaction Saved')

            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        # if transaction is data is not valid
        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
