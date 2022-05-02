import decimal
import time
from datetime import datetime, timedelta
from datetime import date
import datetime as dt

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from accounts.models import Account
from core import settings
from core.util.constants import Disbursement as D, Status
from core.util.constants import Reason as R
from core.util.constants import Status as S
from core.util.decorators import AdminsOnly
from core.util.util_functions import (get_transaction_status, make_payment,
                                      receive_payment)

from .models import Disbursement, Product, Service, Transaction, Wallet


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
        balance = 0
        for wallet in Wallet.objects.filter(holder=request.user):
            balance += wallet.get_wallet_balance()
        context = {
            'num_of_services': num_of_services,
            'num_of_services_this_week': num_of_services_this_week,
            'num_of_services_this_month': num_of_services_this_month,
            'num_of_products': num_of_products,
            'num_of_transactions': num_of_transactions,
            'num_of_transactions_this_week': num_of_transactions_this_week,
            'num_of_transactions_this_month': num_of_transactions_this_month,
            'balance': balance
        }
        return render(request, self.template_name, context)


class TransactionListView(PermissionRequiredMixin, View):
    template_name = 'dashboard/transactions.html'
    permission_required = [
        'dashboard.view_transaction',
    ]

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


class CustomerListView(PermissionRequiredMixin, View):
    template_name = 'dashboard/customer_list.html'
    permission_required = [
        'accounts.view_customer',
    ]

    @method_decorator(AdminsOnly)
    def get(self, request, *args, **kwargs):
        customers = Account.objects.filter(is_customer=True).order_by('-id')
        context = {
            'customers': customers
        }
        return render(request, self.template_name, context)


class CustomerDetailView(PermissionRequiredMixin, View):
    template_name = 'dashboard/customer_detail.html'
    permission_required = [
        'accounts.view_customer',
    ]

    @method_decorator(AdminsOnly)
    def get(self, request, customer_id, *args, **kwargs):
        customer = Account.objects.filter(
            customer_merchant_id=customer_id).first()
        context = {
            'customer': customer,
        }
        return render(request, self.template_name, context)

    @method_decorator(AdminsOnly)
    def post(self, request, *args, **kwargs):
        customer_id = request.POST.get('customer_id')
        customer = Account.objects.filter(
            customer_merchant_id=customer_id).first()
        status = request.POST.get('status')
        if customer is not None:
            if status == Status.APPROVED.value:
                customer.is_active = True
                customer.save()
                messages.success(
                    request, 'Customer Account Activated Successfully!')
            else:
                customer.is_active = False
                customer.save()
                messages.success(
                    request, 'Customer Account Disabled Successfully!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'Customer Not Found!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class DeleteCustomerView(PermissionRequiredMixin, View):
    permission_required = [
        'accounts.view_customer',
        'accounts.delete_customer',
    ]

    @method_decorator(AdminsOnly)
    def get(self, request, *args, **kwargs):
        return redirect('dashboard:customers')

    @method_decorator(AdminsOnly)
    def post(self, request, *args, **kwargs):
        customer_id = request.POST.get('customer_id')
        customer = Account.objects.filter(
            customer_merchant_id=customer_id).first()
        if customer is not None:
            customer.delete()
            messages.success(
                request, 'Customer Account Deleted Successfully!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'Customer Not Found!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class LabourerListView(PermissionRequiredMixin, View):
    template_name = 'dashboard/labourer_list.html'
    permission_required = [
        'accounts.view_labourer',
    ]

    @method_decorator(AdminsOnly)
    def get(self, request, *args, **kwargs):
        labourers = Account.objects.filter(is_labourer=True).order_by('-id')
        context = {
            'labourers': labourers,
        }
        return render(request, self.template_name, context)


class LabourerDetailsView(PermissionRequiredMixin, View):
    template_name = 'dashboard/labourer_detail.html'
    permission_required = [
        'accounts.view_labourer',
    ]

    @method_decorator(AdminsOnly)
    def get(self, request, labourer_id, *args, **kwargs):
        labourer = Account.objects.filter(
            customer_merchant_id=labourer_id).first()
        context = {
            'labourer': labourer,
        }
        return render(request, self.template_name, context)

    @method_decorator(AdminsOnly)
    def post(self, request, *args, **kwargs):
        labourer_id = request.POST.get('labourer_id')
        labourer = Account.objects.filter(
            customer_merchant_id=labourer_id).first()
        status = request.POST.get('status')
        if status == Status.APPROVED.value:
            labourer.is_labourer = True
            labourer.labourer_status = Status.APPROVED.value
            labourer.save()
            messages.success(request, 'Labourer approved successfully')
        elif status == Status.REJECTED.value:
            labourer.is_labourer = False
            labourer.labourer_status = Status.REJECTED.value
            labourer.save()
            messages.success(request, 'Labourer rejected successfully')
        elif status == Status.PENDING.value:
            labourer.is_labourer = False
            labourer.labourer_status = Status.PENDING.value
            labourer.save()
            messages.success(request, 'Labourer status set to pending!')
        else:
            messages.error(request, 'Invalid status choice!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class DeleteLabourerView(PermissionRequiredMixin, View):
    permission_required = [
        'accounts.view_labourer',
        'accounts.delete_labourer',
    ]

    @method_decorator(AdminsOnly)
    def get(self, request, *args, **kwargs):
        return redirect('dashboard:labourers')

    @method_decorator(AdminsOnly)
    def post(self, request, *args, **kwargs):
        labourer_id = request.POST.get('labourer_id')
        labourer = Account.objects.filter(
            customer_merchant_id=labourer_id).first()
        if labourer is not None:
            labourer.delete()
            messages.success(request, 'Labourer deleted successfully!')
        else:
            messages.error(request, 'Labourer not found!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class AdminListView(PermissionRequiredMixin, View):
    template_name = 'dashboard/admin_list.html'
    permission_required = [
        'accounts.view_admin',
    ]

    @method_decorator(AdminsOnly)
    def get(self, request, *args, **kwargs):
        admins = Account.objects.filter(
            Q(is_superuser=True) | Q(is_staff=True)
        ).order_by('-id')
        context = {
            'admins': admins,
        }
        return render(request, self.template_name, context)


class AdminDetailView(PermissionRequiredMixin, View):
    template_name = 'dashboard/admin_detail.html'
    permission_required = [
        'accounts.view_admin',
    ]

    @method_decorator(AdminsOnly)
    def get(self, request, staff_id, *args, **kwargs):
        staff = Account.objects.filter(
            customer_merchant_id=staff_id).first()
        context = {
            'staff': staff,
        }
        return render(request, self.template_name, context)

    @method_decorator(AdminsOnly)
    def post(self, request, *args, **kwargs):
        admin_id = request.POST.get('admin_id')
        admin = Account.objects.filter(
            customer_merchant_id=admin_id).first()
        status = request.POST.get('status')
        if admin is not None:
            if status == Status.APPROVED.value:
                admin.is_active = True
                admin.save()
                messages.success(
                    request, 'Admin Account Activated Successfully!')
            else:
                admin.is_active = False
                admin.save()
                messages.success(
                    request, 'Admin Account Disabled Successfully!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'Admin Not Found!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class DeleteAdminView(PermissionRequiredMixin, View):
    permission_required = [
        'accounts.view_admin',
        'accounts.delete_admin',
    ]

    @method_decorator(AdminsOnly)
    def get(self, request, *args, **kwargs):
        '''Only accepts post requests | Redirects to admin list page upon get request'''
        return redirect('dashboard:admins')

    @method_decorator(AdminsOnly)
    def post(self, request, *args, **kwargs):
        staff_id = request.POST.get('admin_id')
        staff = Account.objects.filter(
            customer_merchant_id=staff_id).first()
        if staff is not None:
            staff.delete()
            messages.success(request, 'Admin Deleted Successfully!')
        else:
            messages.error(request, 'Admin Not Found!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ReceivePaymentView(PermissionRequiredMixin, View):
    template_name = 'dashboard/receive_payment.html'
    permission_required = [
        'dashboard.receive_payment',
    ]

    def generate_transaction_id(self):
        return int(round(time.time() * 1000))

    @method_decorator(AdminsOnly)
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)

    @method_decorator(AdminsOnly)
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


class MakePaymentView(PermissionRequiredMixin, View):
    template_name = 'dashboard/make_payment.html'
    permission_required = [
        'dashboard.make_payment',
    ]

    def generate_transaction_id(self):
        return int(round(time.time() * 1000))

    @method_decorator(AdminsOnly)
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)

    @method_decorator(AdminsOnly)
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


class DisburseToMerchantView(PermissionRequiredMixin, View):
    template_name = 'dashboard/credit_debit_merchant.html'
    permission_required = [
        'dashboard.credit_merchant',
        'dashboard.debit_merchant',
    ]

    @method_decorator(AdminsOnly)
    def get(self, request, *args, **kwargs):
        merchants = Account.objects.filter(
            Q(is_staff=True) | Q(is_superuser=True) | Q(is_labourer=True)
        )

        context = {
            'merchants': merchants,
        }
        return render(request, self.template_name, context)

    @method_decorator(AdminsOnly)
    def post(self, request, *args, **kwargs):
        disbursement_type = request.POST.get('disbursement_type')
        merchant = Account.objects.filter(
            customer_merchant_id=request.POST.get('merchant_id')).first()
        wallet = Wallet.objects.filter(holder=merchant).first()
        amount = request.POST.get('amount')
        note = request.POST.get('note')
        if disbursement_type == D.CREDIT.value:  # Disbursement status is imported as D
            if wallet and merchant:
                wallet.credit_wallet(amount)
                wallet.save()
                disbursement = Disbursement.objects.create(
                    amount=amount,
                    wallet=wallet,
                    disburser=request.user,
                    note=note,
                    modified_by=request.user,
                    disbursement_type=D.CREDIT.value,
                    reason=R.CREDIT_SUCCESSFUL.value,
                    status=S.COMPLETED.value,   # Status is imported as S
                )
                disbursement.save()
                messages.success(request, 'Credit Successful!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(
                    request, "Something went wrong! Couldn't Credit Wallet")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        elif disbursement_type == D.DEBIT.value:
            if merchant and wallet:
                wallet.debit_wallet(amount)
                wallet.save()
                disbursement = Disbursement.objects.create(
                    amount=amount,
                    wallet=wallet,
                    disburser=request.user,
                    note=note,
                    modified_by=request.user,
                    disbursement_type=D.CREDIT.value,
                    reason=R.DEBIT_SUCCESSFUL.value,
                    status=S.COMPLETED.value,   # Status is imported as S
                )
                disbursement.save()
                messages.success(request, 'Debit Successful!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(
                    request, "Something went wrong! Couldn't Debit Wallet")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'Invalid Disbursement Type')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class WalletListView(PermissionRequiredMixin, View):
    template_name = 'dashboard/wallet_list.html'
    permission_required = [
        'dashboard.view_wallet',
    ]

    @method_decorator(AdminsOnly)
    def get(self, request, *args, **kwargs):
        wallets = Wallet.objects.all().order_by('-id')
        context = {'wallets': wallets}
        return render(request, self.template_name, context)


class DisbursementListView(PermissionRequiredMixin, View):
    template_name = 'dashboard/disbursements.html'
    permission_required = [
        'dashboard.view_disbursement',
    ]

    @method_decorator(AdminsOnly)
    def get(self, request, *args, **kwargs):
        disbursements = Disbursement.objects.all().order_by('-id')
        context = {'disbursements': disbursements}
        return render(request, self.template_name, context)


class CashoutView(PermissionRequiredMixin, View):
    template_name = 'dashboard/cashout.html'
    permission_required = [
        'dashboard.cashout',
    ]

    def generate_transaction_id(self):
        '''Generate random Transaction ID from current time in seconds.'''
        return int(round(time.time() * 1000))

    @method_decorator(AdminsOnly)
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)

    @method_decorator(AdminsOnly)
    def post(self, request, *args, **kwargs):
        print('the payment is being processed')
        phone = request.POST.get('phone')
        network = request.POST.get('network')
        transaction_id = self.generate_transaction_id()
        amount = request.POST.get('amount')
        wallet = Wallet.objects.filter(holder=request.user).first()
        data = {
            'transaction_id': transaction_id,
            'mobile_number': phone,
            'amount': amount,
            'wallet_id': settings.WALLET_ID,
            'network_code': network,
            'note': 'Cashout',
        }

        if wallet:
            '''Create disbursement'''
            disbursement = Disbursement.objects.create(
                amount=amount,
                wallet=wallet,
                disburser=request.user,
                note='cashout',
                modified_by=request.user,
                disbursement_type=D.CASHOUT.value,
                reason=R.CASHOUT_SUCCESSFUL.value,
                status=S.PROCESSING.value,   # Status is imported as S
            )
            disbursement.save()

            '''If customer has enough balance - proceed to cashout'''
            if decimal.Decimal(amount) > 0 and wallet.get_wallet_balance() >= decimal.Decimal(amount):
                '''Pay money to user's momo'''
                response = make_payment(data)
                wallet.debit_available_balance(amount)
                wallet.save()
                messages.success(request, 'Cashout Successful!')
                # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif decimal.Decimal(amount) > 0 and wallet.get_wallet_balance() < decimal.Decimal(amount):
                messages.error(
                    request, "You don't have enough balance to cashout")
                # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(
                request, 'Something went wrong! Couldn\'t Cashout')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        response = make_payment(data)
        transaction_status = get_transaction_status(transaction_id)
        '''NOTE: Remember to update the customer and labourer'''
        transaction = {
            'transaction_id': transaction_id,
            'amount': amount,
            'from_phone': phone,
            'network': network,
            'note': 'Cashout',
            'payment_status_code': transaction_status['status_code'],
            'payment_status': transaction_status['message'],
            'customer': request.user,
            'labourer': request.user,
        }
        Transaction.objects.create(**transaction)
        if transaction_status['success'] == True:
            wallet.debit_main_balance(amount)
            wallet.save()
            disbursement.status = S.SUCCESSFUL.value
            disbursement.save()
            messages.success(request, 'Cashout Successful!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            disbursement.status = S.FAILED.value
            disbursement.reason = R.CASHOUT_FAILED.value
            disbursement.save()
            messages.error(
                request, 'Something went wrong! Couldn\'t Cashout')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class JobsListView(PermissionRequiredMixin, View):
    template_name = 'dashboard/jobs.html'
    permission_required = [
        'dashboard.view_service',
    ]

    @method_decorator(AdminsOnly)
    def get(self, request, *args, **kwargs):
        jobs = Service.objects.all().order_by('-id')
        context = {'jobs': jobs}
        return render(request, self.template_name, context)


class JobsTodayView(PermissionRequiredMixin, View):
    template_name = 'dashboard/jobs_today.html'
    permission_required = [
        'dashboard.view_service',
    ]

    @method_decorator(AdminsOnly)
    def get(self, request, *args, **kwargs):
        jobs = Service.objects.filter(
            date_of_service__date=date.today()).order_by('-id')
        context = {'jobs': jobs}
        return render(request, self.template_name, context)


class CompletedJobsView(PermissionRequiredMixin, View):
    template_name = 'dashboard/completed_jobs.html'
    permission_required = [
        'dashboard.view_service',
    ]

    @method_decorator(AdminsOnly)
    def get(self, request, *args, **kwargs):
        jobs = Service.objects.filter(
            status=S.COMPLETED.value).order_by('-id')
        context = {'jobs': jobs}
        return render(request, self.template_name, context)


class PendingJobsView(PermissionRequiredMixin, View):
    template_name = 'dashboard/pending_jobs.html'
    permission_required = [
        'dashboard.view_service',
    ]

    @method_decorator(AdminsOnly)
    def get(self, request, *args, **kwargs):
        jobs = Service.objects.exclude(
            status=S.COMPLETED.value).order_by('-id')
        context = {'jobs': jobs}
        return render(request, self.template_name, context)
