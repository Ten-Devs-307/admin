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
    path('customer-detail/<str:customer_id>/',
         views.CustomerDetailView.as_view(), name='customer_details'),
    path('delete-customer/', views.DeleteCustomerView.as_view(),
         name='delete_customer'),

    path('labourers/', views.LabourerListView.as_view(), name='labourers'),
    path('labourer-detail/<str:labourer_id>/',
         views.LabourerDetailsView.as_view(), name='labourer_details'),
    path('delete-labourer/', views.DeleteLabourerView.as_view(),
         name='delete_labourer'),

    path('administrators/', views.AdminListView.as_view(), name='admins'),
    path('staff-detail/<str:staff_id>/',
         views.AdminDetailView.as_view(), name='admin_details'),
    path('delete-staff/', views.DeleteAdminView.as_view(), name='delete_staff'),

    path('make-disbursement/', views.DisburseToMerchantView.as_view(),
         name='disburse_to_merchant'),
    path('cashout/', views.CashoutView.as_view(), name='cashout'),

    path('wallets/', views.WalletListView.as_view(), name='wallets'),
    path('disbursements/', views.DisbursementListView.as_view(), name='disbursements'),

    path('jobs-today/', views.JobsTodayView.as_view(), name='jobs_today'),
    path('completed-jobs/', views.CompletedJobsView.as_view(), name='completed_jobs'),
    path('pending-jobs/', views.PendingJobsView.as_view(), name='pending_jobs'),

    #     path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('change-password/', views.ChangePasswordView.as_view(),
         name='change_password'),
]
