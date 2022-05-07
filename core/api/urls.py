from django.urls import path
from knox import views as knox_views

from accounts import views as AccountViews

from . import views as APIViews
from .views import LoginAPI

app_name = 'api'
urlpatterns = [
    path('sign-up/', APIViews.RegisterAPI.as_view(), name='sign_up'),

    # knox login, logout
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),

    path('endpoints/', APIViews.APIOverView.as_view(), name='api_overview'),
    path('accounts/', APIViews.AccountList.as_view(), name='account_list'),
    path('products/', APIViews.ProductList.as_view(), name='product_list'),
    path('wallets/', APIViews.WalletList.as_view(), name='wallet_list'),
    path('jobs/', APIViews.JobsList.as_view(), name='jobs'),
    path('transactions/', APIViews.TransactionList.as_view(),
         name='transaction_list'),

    path('job-categories/', APIViews.JobCategoryAPI.as_view(),
         name='job_categories'),
    path('accept-decline-job/<int:pk>/',
         APIViews.AcceptDeclineJob.as_view(), name='accept_decline_job'),
    path('cancel-job/<int:pk>/', APIViews.CancelJob.as_view(), name='cancel_job'),

    path('make-payment/<int:pk>/',
         APIViews.MakePaymentAPI.as_view(), name='make_payment'),

    path('user/<int:pk>/', APIViews.AccountDetail.as_view(), name='user'),
    path('product/<int:pk>/', APIViews.ProductDetail.as_view(), name='product'),
    path('wallet/<int:pk>/', APIViews.WalletDetail.as_view(), name='wallet'),
    path('job/<int:pk>/', APIViews.JobDetail.as_view(), name='service'),
    path('transaction/<int:pk>/',
         APIViews.TransactionDetail.as_view(), name='transaction'),


]
