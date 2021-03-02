# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2021-02-26 05:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('connector', '0006_auto_20210223_1138'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChequeDishonorDetails',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True, db_column=b'DJCREATEDDATE')),
                ('modified_date', models.DateTimeField(auto_now=True, db_column=b'DJMODIFIEDDATE', null=True)),
                ('is_sync', models.BooleanField(db_column=b'ISSYNC', default=False)),
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('bounce_date', models.DateField(blank=True, db_column='BOUNDT', null=True)),
                ('cheque_no', models.CharField(blank=True, db_column='CHQNO', max_length=15, null=True)),
                ('cheque_date', models.DateField(blank=True, db_column='CHQDATE', null=True)),
                ('customer_code', models.IntegerField(blank=True, db_column='CUSTCODE', null=True)),
                ('cheque_amount', models.IntegerField(blank=True, db_column='CHQAMT', null=True)),
                ('bank_name', models.CharField(blank=True, db_column='BANKNAME', max_length=50, null=True)),
                ('created_user', models.CharField(blank=True, db_column='CRETUSER', max_length=10, null=True)),
                ('creation_date', models.DateField(blank=True, db_column='CRETDATE', null=True)),
                ('modified_user', models.CharField(blank=True, db_column='MODIUSER', max_length=10, null=True)),
                ('modi_date', models.DateField(blank=True, db_column='MODIDATE', null=True)),
                ('remarks', models.CharField(blank=True, db_column='REMRKS', max_length=55, null=True)),
                ('rmasid', models.IntegerField(blank=True, db_column='RMASID', default=0)),
                ('bounsid', models.IntegerField(blank=True, db_column='BOUNSID', default=0)),
                ('receipt_number', models.IntegerField(blank=True, db_column='RECPTNO', default=0)),
                ('recept_date', models.DateField(blank=True, db_column='RECPTDT', null=True)),
                ('other_charges', models.FloatField(blank=True, db_column='OTHER_CHGS', null=True)),
                ('c_flag', models.IntegerField(blank=True, db_column='CFLAG', null=True)),
                ('created_by', models.ForeignKey(blank=True, db_column=b'DJCREATEDBY', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_chequedishonordetails_set', to=settings.AUTH_USER_MODEL)),
                ('depo_code', models.ForeignKey(db_column='DEPOCODE', on_delete=django.db.models.deletion.CASCADE, to='connector.DepoMaster')),
                ('modified_by', models.ForeignKey(blank=True, db_column=b'DJMODIFIEDBY', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modified_chequedishonordetails_set', to=settings.AUTH_USER_MODEL)),
                ('recept_id', models.ForeignKey(blank=True, db_column='COLHDRID', null=True, on_delete=django.db.models.deletion.CASCADE, to='connector.CollectionHeader')),
            ],
            options={
                'db_table': 'GCP_FT107_DIS_CHQ',
                'verbose_name_plural': 'CHEQUE DETAILS',
            },
        ),
        migrations.AddField(
            model_name='invoiceheader',
            name='grn_flag',
            field=models.IntegerField(blank=True, db_column='GRNFLAG', default=0, null=True),
        ),
        migrations.AddField(
            model_name='invoiceheader',
            name='tot_grnvalue',
            field=models.IntegerField(blank=True, db_column='TOT_GRNVALUE', default=0, null=True),
        ),
    ]