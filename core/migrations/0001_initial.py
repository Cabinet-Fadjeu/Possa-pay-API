# Generated by Django 5.1.2 on 2024-10-28 15:39

import django.core.validators
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cagnotte',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('name_cagnotte', models.CharField(blank=True, max_length=150, null=True)),
                ('code', models.CharField(blank=True, max_length=8, null=True, unique=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'", regex='^\\+?1?\\d{9,15}$')])),
                ('chosen_currency', models.CharField(blank=True, choices=[('USD', 'USD'), ('XAF', 'XAF'), ('EUR', 'EUR')], default='EUR', max_length=5, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('date_created', models.DateField(auto_now_add=True, null=True, verbose_name='Date Joined')),
                ('cagnotte_status', models.CharField(choices=[('ENCOURS', 'Encours'), ('SOUMISSION', 'Soumission'), ('PAYEE', 'Payee')], default='ENCOURS', max_length=20)),
                ('etat', models.BooleanField(blank=True, default=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('cagnotte_file', models.CharField(blank=True, max_length=250, null=True)),
            ],
            options={
                'ordering': ('-date_created',),
            },
        ),
        migrations.CreateModel(
            name='ContributionCagnotte',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('contribution', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('currency', models.CharField(blank=True, max_length=5, null=True)),
                ('date_created', models.DateField(auto_now_add=True, null=True, verbose_name='Date Joined')),
            ],
            options={
                'ordering': ('-date_created',),
            },
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('first_name', models.CharField(blank=True, max_length=250, null=True, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=250, null=True, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=250, verbose_name='email')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='User amount')),
                ('deposite_type', models.CharField(max_length=250, verbose_name='Deposite type')),
                ('is_Anonymous', models.BooleanField(default=False, verbose_name='Is anonymous')),
                ('deposite_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='recharge date')),
            ],
        ),
        migrations.CreateModel(
            name='ExchageRate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('base', models.CharField(blank=True, max_length=6, null=True, verbose_name='Base')),
                ('rates', models.CharField(blank=True, max_length=5, null=True, verbose_name='Rates')),
                ('values', models.CharField(blank=True, max_length=5, null=True, verbose_name='Values')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('transaction_status', models.CharField(blank=True, choices=[('UNPAID', 'Unpaid'), ('PAID', 'Paid'), ('CANCELLED', 'Cancelled')], default='UNPAID', max_length=15, null=True)),
                ('f_name_participant', models.CharField(blank=True, max_length=150, null=True, verbose_name='Participant F_Name')),
                ('l_name_participant', models.CharField(blank=True, max_length=150, null=True, verbose_name='Participant L_Name')),
                ('email_participant', models.EmailField(blank=True, max_length=250, null=True, verbose_name='Participant Email')),
                ('phone_number', models.CharField(blank=True, max_length=17, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'", regex='^\\+?1?\\d{9,15}$')], verbose_name='Phone Number')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Contribution')),
                ('contribution_method', models.CharField(choices=[('CARTE_CREDIT', 'Carte de Credit'), ('PAYPAL', 'Paypal'), ('ORANGE_MONEY', 'Orange Money'), ('MTN_MOMO', 'MTN MoMo'), ('SMALL_POSSA', 'Small Possa')], default='CARTE_CREDIT', max_length=100)),
                ('currency', models.CharField(blank=True, choices=[('USD', 'USD'), ('XAF', 'XAF'), ('EUR', 'EUR')], default='EUR', max_length=5, null=True)),
                ('is_Anonymous', models.BooleanField(default=False, verbose_name='Is Anonymous')),
                ('date_participate', models.DateTimeField(auto_now_add=True, verbose_name='Date Participated')),
            ],
            options={
                'ordering': ['-date_participate'],
            },
        ),
        migrations.CreateModel(
            name='PoolRetreat',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('retreat_status', models.CharField(blank=True, choices=[('UNHANDLED', 'Unhandled'), ('HANDLED', 'Handled'), ('CANCELLED', 'Cancelled')], default='UNHANDLED', max_length=15, null=True, verbose_name='Retreat Status')),
                ('entered_amt', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Entered Amount')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='amount')),
                ('currency', models.CharField(blank=True, choices=[('USD', 'USD'), ('XAF', 'XAF'), ('EUR', 'EUR')], default='EUR', max_length=5, null=True)),
                ('commission', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Commission')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Completed')),
                ('date_handled', models.DateTimeField(blank=True, null=True, verbose_name='Date Completed')),
                ('requestor_email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Requestor email')),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='RechargeWallet',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('account_email', models.EmailField(blank=True, max_length=250, null=True, verbose_name='Account email')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='User amount')),
                ('sender_email', models.EmailField(blank=True, max_length=250, null=True, verbose_name='Sender email')),
                ('recharge_method', models.CharField(blank=True, max_length=250, null=True, verbose_name='recharge method')),
                ('recharge_status', models.BooleanField(default=False, verbose_name='recharge status')),
                ('recharge_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='recharge date')),
            ],
        ),
        migrations.CreateModel(
            name='Retreat',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('issuer', models.CharField(blank=True, max_length=250, null=True, verbose_name='issuer')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Requested amount')),
                ('currency', models.CharField(blank=True, max_length=5, null=True, verbose_name='last name')),
                ('retreat_type', models.CharField(blank=True, max_length=250, null=True, verbose_name='Retreat Type')),
                ('retreat_info', models.TextField(blank=True, null=True)),
                ('state', models.CharField(blank=True, choices=[('PENDING', 'PENDING'), ('COMPLETED', 'COMPLETED'), ('REJECTED', 'REJECTED')], default='PENDING', max_length=10, null=True)),
                ('request_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='request date')),
                ('issued_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Name')),
                ('title', models.CharField(blank=True, max_length=100, null=True, verbose_name='Title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('profile_img', models.ImageField(blank=True, default=None, null=True, upload_to='reviews/')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='User amount')),
                ('receiver_email', models.EmailField(max_length=250, verbose_name='receiver adress')),
                ('transfer_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='transfer date')),
                ('message', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
