# Generated by Django 4.0.3 on 2022-05-02 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0017_service_published_alter_service_job_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='job_id',
            field=models.CharField(default='d7k1ewbli0', max_length=12),
        ),
    ]
