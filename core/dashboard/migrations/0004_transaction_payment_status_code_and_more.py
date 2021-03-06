# Generated by Django 4.0.3 on 2022-04-05 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_rename_payment_transaction_payment_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='payment_status_code',
            field=models.CharField(default='001', max_length=10),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='payment_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Payment date'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='payment_mode',
            field=models.CharField(default='MOMO', max_length=50, verbose_name='Mode of Payment'),
        ),
    ]
