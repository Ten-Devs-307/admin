from django.urls import path
from accounts import views as AccountViews
from . import views as APIViews

app_name = 'api'
urlpatterns = [
    path('sign-up/', APIViews.SignUp.as_view(), name='sign_up'),

    path('endpoints/', APIViews.APIOverView.as_view(), name='api_overview'),
    path('accounts/', APIViews.AccountList.as_view(), name='account_list'),
    path('products/', APIViews.ProductList.as_view(), name='product_list'),
    path('wallets/', APIViews.WalletList.as_view(), name='wallet_list'),
    path('services/', APIViews.ServiceList.as_view(), name='service_list'),
    path('transactions/', APIViews.TransactionList.as_view(),
         name='transaction_list'),

    path('user/<int:pk>/', APIViews.AccountDetail.as_view(), name='user'),
    path('product/<int:pk>/', APIViews.ProductDetail.as_view(), name='product'),
    path('wallet/<int:pk>/', APIViews.WalletDetail.as_view(), name='wallet'),
    path('service/<int:pk>/', APIViews.ServiceDetail.as_view(), name='service'),
    path('transaction/<int:pk>/',
         APIViews.TransactionDetail.as_view(), name='transaction'),


]
