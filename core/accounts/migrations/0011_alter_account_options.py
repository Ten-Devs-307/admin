# Generated by Django 4.0.3 on 2022-04-18 20:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_account_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'permissions': [('change_account_status', 'Can Change Status Of Account'), ('view_customer', 'Can View Customer'), ('view_labourer', 'Can View Labourer'), ('view_admin', 'Can View Admins'), ('delete_labourer', 'Can Delete Labourer'), ('delete_admin', 'Can Delete Staff Member'), ('delete_customer', 'Can Delete Customer')]},
        ),
    ]
