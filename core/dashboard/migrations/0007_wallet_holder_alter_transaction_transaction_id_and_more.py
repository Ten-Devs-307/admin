# Generated by Django 4.0.3 on 2022-04-18 09:27

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import dashboard.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0006_alter_transaction_wallet'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='holder',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='account_holder', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_id',
            field=models.CharField(default=dashboard.models.Transaction.generate_transaction_id, max_length=50, verbose_name='Wallet ID'),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='wallet_id',
            field=models.CharField(default=uuid.uuid4, max_length=100, verbose_name='Wallet ID'),
        ),
    ]
