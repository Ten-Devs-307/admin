# Generated by Django 4.0.3 on 2022-04-18 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_account_customer_id_account_location_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'permissions': [('disable_account', 'Can disable account')]},
        ),
        migrations.AlterModelTable(
            name='account',
            table='accounts',
        ),
    ]
