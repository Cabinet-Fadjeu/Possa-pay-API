# Generated by Django 5.1.3 on 2024-12-29 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_transaction_from_country_transaction_to_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='frais',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='fees Amount'),
        ),
    ]
