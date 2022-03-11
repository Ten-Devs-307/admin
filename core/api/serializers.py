from rest_framework import serializers
from accounts.models import Account
from dashboard.models import Transaction, Product, Wallet, Service


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        # fields = "__all__"
        exclude = ('password', 'user_permissions', 'groups', 'is_superuser',
                   'is_staff', 'is_active', 'last_login')


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"
