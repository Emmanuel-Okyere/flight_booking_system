# Generated by Django 4.0.6 on 2022-08-11 16:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, null=True)),
                ('currency', models.CharField(default='GHS', max_length=50)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[(0, 'deposit'), (1, 'transfer'), (2, 'withdraw')], max_length=200, null=True)),
                ('receipt', models.IntegerField()),
                ('amount_credited', models.DecimalField(decimal_places=2, max_digits=200)),
                ('customer_name', models.CharField(max_length=250)),
                ('customer_number', models.IntegerField()),
                ('payment_status', models.CharField(choices=[(0, 'paid'), (1, 'pending'), (2, 'not sucess')], max_length=200, null=True)),
                ('paystack_payment_reference', models.CharField(blank=True, default='', max_length=100)),
                ('wallet', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='payment.wallet')),
            ],
        ),
    ]
