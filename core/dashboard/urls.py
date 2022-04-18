from django.urls import path
from . import views

app_name = 'dashboard'
urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('transactions/', views.TransactionListView.as_view(), name='transactions'),
    path('receive-payment/', views.ReceivePaymentView.as_view(),
         name='receive_payment'),
    path('make-payment/', views.MakePaymentView.as_view(), name='make_payment'),

    path('customers/', views.CustomerListView.as_view(), name='customers'),
    path('labourers/', views.LabourerListView.as_view(), name='labourers'),
    path('labourer-detail/<str:labourer_id>/',
         views.LabourerDetailsView.as_view(), name='labourer_details'),
    path('customer-detail/<str:customer_id>/',
         views.CustomerDetailView.as_view(), name='customer_details'),
    path('staff-detail/<str:staff_id>/',
         views.AdminDetailView.as_view(), name='admin_details'),
    path('administrators/', views.AdminListView.as_view(), name='admins'),
]
