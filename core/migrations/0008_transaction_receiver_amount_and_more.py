# Generated by Django 5.1.3 on 2025-01-06 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_transaction_frais'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='receiver_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Receiver Amount'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='receiver_currency',
            field=models.CharField(blank=True, choices=[('USD', 'USD'), ('XAF', 'XAF'), ('EUR', 'EUR')], max_length=5, null=True),
        ),
    ]
