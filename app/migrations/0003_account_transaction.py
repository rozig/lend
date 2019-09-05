# Generated by Django 2.2.4 on 2019-08-28 00:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20190825_2131'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('number', models.CharField(blank=True, max_length=10, primary_key=True, serialize=False, unique=True)),
                ('balance', models.FloatField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Account',
                'verbose_name_plural': 'Accounts',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('id', models.CharField(blank=True, max_length=12, primary_key=True, serialize=False, unique=True)),
                ('type', models.CharField(max_length=10)),
                ('amount', models.FloatField()),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Account')),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
            },
        ),
    ]