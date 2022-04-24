import imp

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.response import Response

from accounts.models import Account
from dashboard.models import (Disbursement, Product, Service, Transaction,
                              Wallet)


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


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('customer_merchant_id', 'name', 'email')


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('email', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Account.objects.create_user(
            name=validated_data['name'], email=validated_data['email'], password=validated_data['password'])

        return user

# class SignUpSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Account
#         fields = ('email', 'name', 'password')
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = Account.objects.create_user(
#             email=validated_data['email'],
#             name=validated_data['name'],
#             password=validated_data['password'],
#         )
#         user.save()
#         return user


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        # authenticate  user
        user = authenticate(**data)
        if user and user.is_active:
            return Response(user, status=200)
        raise Response(
            {"error": "Unable to log in with provided credentials."}, status=400)


class CashoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('amount', 'note', 'disburser', 'disbursement_type', 'status')

    def create(self, validated_data):
        transaction = Transaction.objects.create(
            amount=validated_data['amount'],
            note=validated_data['note'],
            disbursement_type=validated_data['disbursement_type'],
        )
        transaction.save()
        return transaction
