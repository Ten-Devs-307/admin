# Generated by Django 4.0.3 on 2022-05-09 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0029_alter_service_job_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='job_id',
            field=models.CharField(default='ool2j8cpkd', max_length=12),
        ),
    ]
