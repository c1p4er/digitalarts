# Generated by Django 4.2.7 on 2024-06-11 12:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0023_alter_shipment_driver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipment',
            name='delivered_at',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
