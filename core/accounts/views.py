from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from accounts.forms import RegisterForm


class LoginView(View):
    template_name = 'accounts/login.html'

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
            return redirect('accounts:login')


class SignUpView(View):
    template_name = 'accounts/sign_up.html'
    form_class = RegisterForm

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect(
                request.META.get("HTTP_REFERER") or "accounts:sign_up")
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(password)
            user.save()
            # login(request, user)
            return redirect(
                request.META.get("HTTP_REFERER"))
        else:
            messages.error(request, "Invalid form")
            return redirect(
                request.META.get("HTTP_REFERER") or "accounts:sign_up")


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('accounts:login')
