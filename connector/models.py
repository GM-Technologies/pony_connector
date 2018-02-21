from __future__ import unicode_literals

from django.db import models

from connector import base_models


class ProductCategory(base_models.AuditModel):
    code = models.IntegerField(primary_key=True, db_column='GRPCODE')
    name = models.CharField(max_length=55, db_column='GRPNAME')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Product Categories"
        db_table = "GCP_SM23_PDT_GRP"


class ProductSubCategory(base_models.AuditModel):
    id = models.IntegerField(primary_key=True, db_column='ID')
    code = models.IntegerField(db_column='SUBGRP')
    category = models.ForeignKey(ProductCategory, db_column='GRPCODE')
    description = models.CharField(max_length=55, db_column='SGRPDESC')

    def __str__(self):
        return self.description

    class Meta:
        verbose_name_plural = "Product SubCategories"
        db_table = "GCP_SM25_PDT_SUG"
        unique_together = ['code', 'category']


class TariffHeader(base_models.AuditModel):
    category = models.OneToOneField(ProductCategory, primary_key=True, db_column='GRPCODE')
    name = models.CharField(max_length=150, db_column='GRPNAME')
    type = models.CharField(max_length=2, db_column='GRPTYPE')

    class Meta:
        verbose_name_plural = "Tariff Header"
        db_table = "GCP_SM27_TARIFF_HDR"


class TariffMaster(base_models.AuditModel):
    tariff_id = models.IntegerField(primary_key=True, db_column='TARIFFID')
    tariff_head = models.CharField(max_length=10, db_column='TARIFFHD')
    description = models.CharField(max_length=80, db_column='TARIFF_DES')
    hsn_code = models.CharField(max_length=8, db_column='HSNCODE')
    gst = models.DecimalField(max_length=5, decimal_places=2, db_column='GSTPER')

    def __str__(self):
        return self.tariff_id

    class Meta:
        verbose_name_plural = "Tariff Master"
        db_table = "GCP_SM27_TARIFF_MAS"


class ProductMaster(base_models.AuditModel):
    product_code = models.IntegerField(primary_key=True, db_column='PRODCODE')
    description = models.CharField(max_length=60, db_column='PRODDESC')
    size = models.CharField(max_length=10, db_column='PSIZE')
    length = models.CharField(max_length=10, db_column='PRODLENG')
    count = models.IntegerField(db_column='PRODCNT')
    unit = models.CharField(max_length=5, db_column='UNIT')
    category = models.ForeignKey(ProductCategory, db_column='GRPCODE')
    sub_category = models.ForeignKey(ProductSubCategory, db_column='SUBGRP')
    tariff = models.ForeignKey(TariffMaster, db_column='TARIFFID')

    def __str__(self):
        return self.product_code

    class Meta:
        verbose_name_plural = "Product Master"
        db_table = "GCP_SM22_PDT"


class Price(base_models.AuditModel):
    id = models.IntegerField(primary_key=True, db_column='ID')
    price_code = models.IntegerField(db_column='PRICECODE')
    with_effect_from = models.DateField(db_column='WEFDATE')
    product_code = models.ForeignKey(ProductMaster, db_column='PRODCODE')
    price = models.IntegerField(db_column='PRODCNT')

    def __str__(self):
        return self.product_code

    class Meta:
        verbose_name_plural = "Price"
        db_table = "GCP_SM62_PRI_DTL"
