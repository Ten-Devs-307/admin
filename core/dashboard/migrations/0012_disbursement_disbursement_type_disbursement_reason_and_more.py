# Generated by Django 4.0.3 on 2022-04-24 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_wallet_date_added_wallet_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='disbursement',
            name='disbursement_type',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='disbursement',
            name='reason',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='disbursement',
            name='status',
            field=models.CharField(default='pending', max_length=200),
        ),
    ]
