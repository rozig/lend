# Generated by Django 2.2.4 on 2019-09-05 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_account_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='description',
            field=models.CharField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='account',
            name='number',
            field=models.CharField(max_length=10, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='id',
            field=models.CharField(max_length=12, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
