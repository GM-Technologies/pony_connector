# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2021-02-13 19:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connector', '0004_paymentadjustmentdetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='NationalPaymentPendingView',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('customer', models.IntegerField(blank=True, db_column='CUSTCODE', null=True)),
                ('invoice_number', models.IntegerField(blank=True, db_column='INVNO', null=True)),
                ('invoice_date', models.DateField(blank=True, db_column='INVDT', null=True)),
                ('invoice_type', models.CharField(blank=True, db_column='INVTYPE', max_length=1, null=True)),
                ('net_amount', models.FloatField(blank=True, db_column='NETAMT', null=True)),
                ('paid_amount', models.FloatField(blank=True, db_column='PAIDAMT', null=True)),
                ('received_amount', models.FloatField(blank=True, db_column='RECDAMT', null=True)),
                ('balance_amount', models.FloatField(blank=True, db_column='BALAMT', null=True)),
                ('customer_name', models.CharField(blank=True, db_column='CUSTNAME', max_length=50, null=True)),
                ('customer_city', models.CharField(blank=True, db_column='CUSTCITY', max_length=35, null=True)),
                ('rmasid', models.IntegerField(blank=True, db_column='MASID', default=0)),
                ('delay_days', models.IntegerField(blank=True, db_column='DELAY', null=True)),
                ('depot', models.IntegerField(blank=True, db_column='DEPOT', null=True)),
                ('other_charges', models.FloatField(blank=True, db_column='OTHER_CHGS', null=True)),
            ],
            options={
                'db_table': 'NATIONAL_PAYMENT_PENDING',
                'verbose_name_plural': 'National Payment View',
            },
        ),
    ]
