from django.http import HttpResponseRedirect
import time
from django.db.models import Q
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from accounts.models import Account

from core import settings
from core.util.decorators import AdminsOnly
from core.util.util_functions import get_transaction_status, make_payment, receive_payment
from .models import Product, Service, Transaction, Wallet
from django.contrib import messages


class DashboardView(View):
    template_name = 'dashboard/dashboard.html'

    @method_decorator(AdminsOnly)
    def get(self, request, *args, **kwargs):
        num_of_services = Service.objects.count()
        num_of_services_this_week = Service.objects.filter(
            date_of_service__gte=datetime.today() - timedelta(days=7)).count()
        num_of_services_this_month = Service.objects.filter(
            date_of_service__gte=datetime.today() - timedelta(days=30)).count()

        num_of_products = Product.objects.count()
        num_of_transactions = Transaction.objects.count()

        num_of_transactions_this_week = Transaction.objects.filter(
            payment_date__gte=datetime.now() - timedelta(days=7)).count()

        num_of_transactions_this_month = Transaction.objects.filter(
            payment_date__gte=datetime.now() - timedelta(days=30)).count()
        context = {
            'num_of_services': num_of_services,
            'num_of_services_this_week': num_of_services_this_week,
            'num_of_services_this_month': num_of_services_this_month,
            'num_of_products': num_of_products,
            'num_of_transactions': num_of_transactions,
            'num_of_transactions_this_week': num_of_transactions_this_week,
            'num_of_transactions_this_month': num_of_transactions_this_month,
        }
        return render(request, self.template_name, context)


class TransactionListView(View):
    template_name = 'dashboard/transactions.html'

    @method_decorator(AdminsOnly)
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        if query:
            transactions = Transaction.objects.filter(
                Q(transaction_id__icontains=query) | Q(customer__name__icontains=query) | Q(labourer__name__icontains=query) | Q(
                    service__icontains=query) | Q(wallet__wallet_id__icontains=query) | Q(payment_mode__icontains=query)
            )
        else:
            transactions = Transaction.objects.all().order_by('-id')
        context = {'transactions': transactions}
        return render(request, self.template_name, context)


class CustomerListView(View):
    template_name = 'dashboard/customer_list.html'

    @method_decorator(AdminsOnly)
    def get(self, request, *args, **kwargs):
        customers = Account.objects.filter(is_customer=True).order_by('-id')
        context = {
            'customers': customers
        }
        return render(request, self.template_name, context)


class LabourerListView(View):
    template_name = 'dashboard/labourer_list.html'

    @method_decorator(AdminsOnly)
    def get(self, request, *args, **kwargs):
        labourers = Account.objects.filter(is_labourer=True).order_by('-id')
        context = {
            'labourers': labourers,
        }
        return render(request, self.template_name, context)


class LabourerDetailsView(View):
    template_name = 'dashboard/labourer_details.html'

    @method_decorator(AdminsOnly)
    def get(self, request, *args, **kwargs):
        labourer_id = request.GET.get('labourer_id')
        labourer = Account.objects.get(id=labourer_id)
        context = {
            'labourer': labourer,
        }
        return render(request, self.template_name, context)


class AdminListView(View):
    template_name = 'dashboard/admin_list.html'

    @method_decorator(AdminsOnly)
    def get(self, request, *args, **kwargs):
        admins = Account.objects.filter(
            Q(is_superuser=True) | Q(is_staff=True)
        ).order_by('-id')
        context = {
            'admins': admins,
        }
        return render(request, self.template_name, context)


class ReceivePaymentView(View):
    template_name = 'dashboard/receive_payment.html'

    def generate_transaction_id(self):
        return int(round(time.time() * 1000))

    @ method_decorator(AdminsOnly)
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)

    @ method_decorator(AdminsOnly)
    def post(self, request, *args, **kwargs):
        print('the payment is being processed')
        user = request.user
        phone = request.POST.get('phone')
        amount = request.POST.get('amount')
        network = request.POST.get('network')
        note = request.POST.get('note')
        transaction_id = self.generate_transaction_id()

        data = {
            'transaction_id': transaction_id,
            'mobile_number': phone,
            'amount': amount,
            'wallet_id': settings.WALLET_ID,
            'network_code': network,
            'note': note,
        }
        response = receive_payment(data)
        # wait for 30 seconds for transaction to be processed
        for i in range(3):
            time.sleep(10)
            transaction_status = get_transaction_status(transaction_id)
            if transaction_status['success'] == True:
                print('the transaction was successful')
                # user.has_paid = True
                break

        transaction = {
            'transaction_id': transaction_id,
            'amount': amount,
            'from_phone': phone,
            'network': network,
            'note': note,
            'payment_status_code': transaction_status['status_code'],
            'payment_status': transaction_status['message'],
            'customer': user,
            'labourer': user,
        }
        Transaction.objects.create(**transaction)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class MakePaymentView(View):
    template_name = 'dashboard/make_payment.html'

    def generate_transaction_id(self):
        return int(round(time.time() * 1000))

    @ method_decorator(AdminsOnly)
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)

    @ method_decorator(AdminsOnly)
    def post(self, request, *args, **kwargs):
        print('the payment is being processed')
        user = request.user
        phone = request.POST.get('phone')
        amount = request.POST.get('amount')
        network = request.POST.get('network')
        note = request.POST.get('note')
        transaction_id = self.generate_transaction_id()

        data = {
            'transaction_id': transaction_id,
            'mobile_number': phone,
            'amount': amount,
            'wallet_id': settings.WALLET_ID,
            'network_code': network,
            'note': note,
        }
        response = make_payment(data)
        # wait for 30 seconds for transaction to be processed
        for i in range(3):
            time.sleep(10)
            transaction_status = get_transaction_status(transaction_id)
            if transaction_status['success'] == True:
                print('the transaction was successful')
                # user.has_paid = True
                break

        transaction = {
            'transaction_id': transaction_id,
            'amount': amount,
            'from_phone': phone,
            'network': network,
            'note': note,
            'payment_status_code': transaction_status['status_code'],
            'payment_status': transaction_status['message'],
            'customer': user,
            'labourer': user,
        }
        Transaction.objects.create(**transaction)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
