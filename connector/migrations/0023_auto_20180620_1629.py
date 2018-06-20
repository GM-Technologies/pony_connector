# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-20 10:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connector', '0022_auto_20180620_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoiceheader',
            name='balance_amount',
            field=models.FloatField(blank=True, db_column='BALAMT', null=True),
        ),
        migrations.AlterField(
            model_name='invoiceheader',
            name='cancel',
            field=models.CharField(blank=True, db_column='CANCEL', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='invoiceheader',
            name='invoice_gstin',
            field=models.CharField(blank=True, db_column='INV_GSTIN', max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='invoiceheader',
            name='remarks',
            field=models.CharField(blank=True, db_column='REMARKS', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='invoiceheader',
            name='total_tax_amount',
            field=models.FloatField(blank=True, db_column='TOT_TAXAMT', null=True),
        ),
    ]
