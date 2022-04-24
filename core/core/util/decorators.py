from django.contrib import messages
from django.shortcuts import HttpResponse, redirect


class AdminsOnly(object):
    def __init__(self, function):
        self.function = function

    def __call__(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_staff:
                return self.function(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorized to view this page")
        else:
            messages.error(request, "You must login to continue!")
            return redirect('accounts:login')
