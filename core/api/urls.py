from django.urls import path
from accounts import views as AccountViews
from . import views as APIViews

app_name = 'api'
urlpatterns = [
    path('endpoints/', APIViews.APIOverView.as_view(), name='api_overview'),
    path('products/', APIViews.ProductList.as_view(), name='product_list'),
    path('services/', APIViews.ServiceList.as_view(), name='service_list'),
    path('transactions/', APIViews.TransactionList.as_view(),
         name='transaction_list'),
    path('accounts/', APIViews.AccountList.as_view(), name='account_list'),
    path('wallets/', APIViews.WalletList.as_view(), name='wallet_list'),
    path('user/<int:pk>/', APIViews.OneUser.as_view(), name='one_user'),
    path('sign-up/', APIViews.SignUp.as_view(), name='sign_up'),
]
