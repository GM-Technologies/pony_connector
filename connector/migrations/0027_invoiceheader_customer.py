# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-20 11:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connector', '0026_auto_20180620_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoiceheader',
            name='customer',
            field=models.IntegerField(blank=True, db_column='CUSTCODE', null=True),
        ),
    ]
