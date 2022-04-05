from django.urls import path
from . import views

app_name = 'dashboard'
urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('transactions/', views.TransactionListView.as_view(), name='transactions'),
    path('make-payment/', views.MakePaymentView.as_view(), name='make_payment'),
]
