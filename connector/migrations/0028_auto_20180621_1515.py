# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-21 09:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('connector', '0027_invoiceheader_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoicedetails',
            name='invoice_header',
            field=models.ForeignKey(db_column='INVHDRID', on_delete=django.db.models.deletion.CASCADE, to='connector.InvoiceHeader'),
        ),
    ]