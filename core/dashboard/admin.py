from django.contrib import admin

from .models import *

admin.site.register(Wallet)
admin.site.register(Transaction)
admin.site.register(Disbursement)
admin.site.register(Service)
admin.site.register(JobCategory)
