# Generated by Django 5.1.3 on 2024-11-18 07:27

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewTransaction',
            fields=[
                ('transaction_id', models.AutoField(primary_key=True, serialize=False)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('patient_name', models.CharField(max_length=50)),
                ('patient_age', models.IntegerField()),
                ('problem', models.CharField(max_length=500)),
                ('products', models.CharField(max_length=500)),
                ('customer_name', models.CharField(max_length=50)),
                ('customer_age', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('patient_id', models.AutoField(primary_key=True, serialize=False)),
                ('patient_name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('sex', models.CharField(max_length=10)),
                ('problem', models.CharField(max_length=1000)),
                ('customer_name', models.CharField(max_length=100)),
                ('customer_age', models.IntegerField(verbose_name=django.core.validators.MinValueValidator(19))),
                ('nic', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=100)),
                ('mrp', models.DecimalField(decimal_places=2, max_digits=10)),
                ('mfg', models.DateField()),
                ('exp', models.DateField()),
                ('qty', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=128, validators=[django.core.validators.RegexValidator(message='Password must contain at least 6 characters with letters and numbers.', regex='^(?=.*[A-Za-z])(?=.*\\d)[A-Za-z\\d]{6,}$')], verbose_name='Password')),
                ('failed_attempts', models.IntegerField(default=0)),
                ('is_blocked', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=20, unique=True)),
                ('date_time', models.DateTimeField()),
                ('customer_name', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='customer_transactions', to='store.patient')),
                ('patient_name', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='patient_transactions', to='store.patient')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100)),
                ('quantity', models.PositiveIntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='store.transaction')),
            ],
        ),
    ]
