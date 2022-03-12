from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from .models import Product, Service, Transaction, Wallet
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


class LoginView(View):
    template_name = 'dashboard/login.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard:dashboard')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('dashboard:login')


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('dashboard:login')


class DashboardView(View):
    template_name = 'dashboard/dashboard.html'

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
