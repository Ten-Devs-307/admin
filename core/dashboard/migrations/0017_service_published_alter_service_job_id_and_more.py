# Generated by Django 4.0.3 on 2022-05-02 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0016_alter_service_job_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='published',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='service',
            name='job_id',
            field=models.CharField(default='zjvxzuarze', max_length=12),
        ),
        migrations.AlterField(
            model_name='service',
            name='mode_of_payment',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='service',
            name='status',
            field=models.CharField(default='pending', max_length=20),
        ),
    ]
