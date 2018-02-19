# from __future__ import unicode_literals
#
# from django.db import models
#
# from connector import base_models
#
#
# class ProductCategory(base_models.AuditModel):
#     name = models.CharField(max_length=30)
#     description = models.TextField()
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name_plural = "Product Categories"
#         db_table = "gm_product_category"
#
#
# class ProductSubCategory(base_models.AuditModel):
#     name = models.CharField(max_length=30)
#     description = models.TextField()
#     category = models.ForeignKey(ProductCategory)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name_plural = "Product SubCategories"
#         db_table = "gm_product_subcategory"
#
#
# class TariffMaster(base_models.AuditModel):
#     tariff_id = models.IntegerField(primary_key=True)
#     tariff_name = models.CharField(max_length=30)
#     tariff_head = models.CharField(max_length=30)
#     hsn_code = models.CharField(max_length=15)
#     gst = models.DecimalField(max_length=5, decimal_places=2)
#     with_effect_date = models.DateField()
#     status = models.BooleanField(default=True)
#
#     def __str__(self):
#         return self.tariff_name
#
#     class Meta:
#         verbose_name_plural = "Tariffs"
#         db_table = "gm_tariff"
#
#
# class ProductMaster(base_models.AuditModel):
#     product_code = models.IntegerField(primary_key=True)
#
#
# class Designation(base_models.AuditModel):
#     designation_id = models.IntegerField(primary_key=True)
#     designation_name = models.CharField(max_length=30)
#     status = models.BooleanField(default=True)
#
#     def __str__(self):
#         return self.designation_name
#
#     class Meta:
#         verbose_name_plural = "Designations"
#         db_table = "gm_designation"
#
#
# class Division(base_models.AuditModel):
#     division_id = models.IntegerField(primary_key=True)
#     division_name = models.CharField(max_length=30)
#     email_id = models.CharField(max_length=30)
#     phone_number = models.CharField(max_length=15)
#     extra_phone_number = models.CharField(max_length=15)
#     address = models.CharField(max_length=100)
#     locality = models.CharField(max_length=20)
#     pincode = models.CharField(max_length=8)
#     status = models.BooleanField(default=True)
#
#     def __str__(self):
#         return self.division_name
#
#     class Meta:
#         verbose_name_plural = "Divisions"
#         db_table = "gm_division"
#
#
# class Depot(base_models.AuditModel):
#     depot_id = models.IntegerField(primary_key=True)
#     division = models.ForeignKey(Division)
#     depot_name = models.CharField(max_length=30)
#     email_id = models.CharField(max_length=30)
#     phone_number = models.CharField(max_length=15)
#     extra_phone_number = models.CharField(max_length=15)
#     address = models.CharField(max_length=100)
#     locality = models.CharField(max_length=20)
#     pincode = models.CharField(max_length=8)
#     price_code = models.ForeignKey(Price)
#     status = models.BooleanField(default=True)
#
#     def __str__(self):
#         return self.depot_name
#
#     class Meta:
#         verbose_name_plural = "Depots"
#         db_table = "gm_depot"