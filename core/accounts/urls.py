from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('sign-up/', views.SignUpView.as_view(), name='sign_up'),
]
