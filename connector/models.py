from __future__ import unicode_literals

import datetime
from django.db import models

from connector import base_models


class ProductCategory(base_models.AuditModel):
    code = models.IntegerField(primary_key=True, db_column='GRPCODE')
    name = models.CharField(max_length=55, db_column='GRPNAME')

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name_plural = "Product Categories"
        db_table = "GCP_SM23_PDT_GRP"

    def to_json(self):
        return {
            "code": str(self.code),
            "name": self.name,
            "is_sync": self.is_sync
        }


class ProductSubCategory(base_models.AuditModel):
    id = models.AutoField(primary_key=True, db_column='ID')
    code = models.IntegerField(db_column='SUBGRP')
    category = models.ForeignKey(ProductCategory, db_column='GRPCODE')
    description = models.CharField(max_length=55, db_column='SGRPDESC')

    def __str__(self):
        return "{}".format(self.code)

    class Meta:
        verbose_name_plural = "Product SubCategories"
        db_table = "GCP_SM25_PDT_SUG"
        unique_together = ['code', 'category']

    def to_json(self):
        return {
            "id": str(self.id),
            "code": str(self.code),
            "category": self.category.to_json(),
            "description": self.description,
            "is_sync": self.is_sync
        }


class TariffMaster(base_models.AuditModel):
    tariff_id = models.IntegerField(primary_key=True, db_column='TARIFFID')
    tariff_header = models.CharField(max_length=100, null=True, db_column='TARIFFHD')
    description = models.CharField(max_length=80, db_column='TARIFF_DES')
    hsn_code = models.CharField(max_length=10, db_column='HSNCODE')
    gst = models.DecimalField(max_digits=5, decimal_places=2, db_column='GSTPER')

    def __str__(self):
        return "{}".format(self.tariff_id)

    class Meta:
        verbose_name_plural = "Tariff Master"
        db_table = "GCP_SM27_TARIFF_MAS"

    def to_json(self):
        return {
            "tariff_id": str(self.tariff_id),
            "tariff_header": self.tariff_header or None,
            "description": self.description,
            "hsn_code": self.hsn_code,
            "gst": str(self.gst),
            "is_sync": self.is_sync
        }


class ProductMaster(base_models.AuditModel):
    product_code = models.IntegerField(primary_key=True, db_column='PRODCODE')
    description = models.CharField(max_length=60, db_column='PRODDESC')
    size = models.CharField(max_length=10, db_column='PSIZE')
    length = models.CharField(max_length=10, db_column='PRODLENG')
    count = models.IntegerField(db_column='PRODCNT', null=True)
    unit = models.CharField(max_length=5, db_column='UNIT')
    category = models.ForeignKey(ProductCategory, db_column='GRPCODE')
    sub_category_code = models.IntegerField(db_column='SUBGRP', null=True, blank=True)
    sub_category = models.ForeignKey(ProductSubCategory, db_column='SUBGRPID')
    tariff = models.ForeignKey(TariffMaster, db_column='TARIFFID')

    def __str__(self):
        return "{}".format(self.product_code)

    class Meta:
        verbose_name_plural = "Product Master"
        db_table = "GCP_SM22_PDT"

    def to_json(self, input_date=datetime.date.today()):
        prices = self.price_set.filter(with_effect_from__lte=input_date)
        current_price = prices.order_by('-with_effect_from')\
            .first().to_json() if prices.exists() else {}
        return {
            "product_code": str(self.product_code),
            "description": self.description,
            "size": self.size,
            "length": self.length,
            "count": str(self.count),
            "unit": self.unit,
            "category": self.category.to_json(),
            "sub_category": self.sub_category.to_json(),
            "tariff": self.tariff.to_json(),
            "price": current_price,
            "is_sync": self.is_sync
        }


class Price(base_models.AuditModel):
    id = models.AutoField(primary_key=True, db_column='ID')
    price_code = models.IntegerField(db_column='PRICECODE')
    with_effect_from = models.DateField(db_column='WEFDATE')
    product_code = models.ForeignKey(ProductMaster, db_column='PRODCODE')
    price = models.FloatField(db_column='PRICE')

    def __str__(self):
        return "{} - {}".format(self.product_code, self.price_code)

    class Meta:
        verbose_name_plural = "Price"
        db_table = "GCP_SM62_PRI_DTL"
        unique_together = ['price_code', 'with_effect_from', 'product_code']

    def to_json(self, with_product=False):
        return {
            "id": str(self.id),
            "price_code": str(self.price_code),
            "with_effect_from": str(self.with_effect_from),
            "product": self.product_code.to_json() if
            with_product else self.product_code.product_code,
            "price": str(self.price),
            "is_sync": self.is_sync
        }


class User(base_models.AuditModel):
    id = models.AutoField(primary_key=True, db_column='ID')
    user_id = models.IntegerField(db_column='USERID')
    user_name = models.CharField(max_length=40, db_column='USERNAME')
    dept_code = models.IntegerField(db_column='DEPTCODE')

    def __str__(self):
        return "{}".format(self.user_id)

    class Meta:
        verbose_name_plural = "User"
        db_table = "GCP_AM03_USR_HDR"


class DivisionMaster(base_models.AuditModel):
    division_code = models.IntegerField(primary_key=True, db_column='DIVNCODE')
    division_name = models.CharField(max_length=25, db_column='DIVNNAME')
    division_add1 = models.CharField(max_length=35, db_column='DIVNADD1')
    division_add2 = models.CharField(max_length=35, db_column='DIVNADD2')
    division_add3 = models.CharField(max_length=35, db_column='DIVNADD3')
    division_pincode = models.CharField(max_length=10, db_column='DIVNPIN')
    division_phonenumber = models.CharField(max_length=60, db_column='DIVNPHNO')
    division_fax = models.CharField(max_length=60, db_column='DIVNFAX')
    division_mail = models.CharField(max_length=25, db_column='DIVNMAIL')

    def __str__(self):
        return "{}".format(self.division_code)

    class Meta:
        verbose_name_plural = "Division Master"
        db_table = "GCP_SM01_DIV"

    def to_json(self):
        return {
            "division_code": str(self.division_code),
            "division_name": self.division_name,
            "division_add1": self.division_add1,
            "division_add2": self.division_add2,
            "division_add3": self.division_add3,
            "division_pincode": self.division_pincode,
            "division_phonenumber": self.division_phonenumber,
            "division_fax": self.division_fax,
            "division_mail": self.division_mail,
            "is_sync": self.is_sync
        }


class DepoMaster(base_models.AuditModel):
    depo_code = models.IntegerField(primary_key=True, db_column='DEPOCODE')
    division_code = models.ForeignKey(DivisionMaster, db_column='DIVNCODE')
    depo_name = models.CharField(max_length=25, db_column='DEPONAME')
    state_code = models.CharField(max_length=2, db_column='STATCODE')
    depo_add1 = models.CharField(max_length=55, db_column='DEPOADD1')
    depo_add2 = models.CharField(max_length=55, db_column='DEPOADD2')
    depo_add3 = models.CharField(max_length=55, db_column='DEPOADD3')
    depo_pincode = models.IntegerField(db_column='DEPOPIN')
    depo_phonenumber = models.CharField(max_length=60, db_column='DEPOPHNO')
    depo_fax = models.CharField(max_length=60, db_column='DEPOFAX')
    depo_mail = models.CharField(max_length=35, db_column='DEPOMAIL')
    gst_registered_date = models.DateField(db_column='GSTREGDT')
    price_code = models.IntegerField(db_column='PRICECOD')
    gstin = models.CharField(max_length=15, db_column='GSTIN')

    def __str__(self):
        return "{}".format(self.depo_code)

    class Meta:
        verbose_name_plural = "Depo Master"
        db_table = "GCP_SM06_DEP"

    def to_json(self, with_division=False):
        return {
            "depo_code": str(self.depo_code),
            "division": self.division_code.to_json() if with_division
            else self.division_code.division_code,
            "depo_name": self.depo_name,
            "state_code": self.state_code,
            "depo_add1": self.depo_add1,
            "depo_add2": self.depo_add2,
            "depo_add3": self.depo_add3,
            "depo_pincode": self.depo_pincode,
            "depo_phonenumber": self.depo_phonenumber,
            "depo_fax": self.depo_fax,
            "depo_mail": self.depo_mail,
            "gst_registered_date": str(self.gst_registered_date),
            "price_code": self.price_code,
            "gstin": self.gstin,
            "is_sync": self.is_sync
        }


class Market(base_models.AuditModel):
    id = models.AutoField(primary_key=True, db_column='ID')
    market_code = models.IntegerField(db_column='MKTCODE')
    depo_code = models.ForeignKey(DepoMaster, db_column='DEPOCODE')
    market_name = models.CharField(max_length=25, db_column='MKTNAME')
    price_code = models.IntegerField(db_column='PRICECOD')

    def __str__(self):
        return "{} - {}".format(self.market_code, self.depo_code)

    class Meta:
        verbose_name_plural = "Market"
        db_table = "GCP_SM03_MKT"
        unique_together = ['market_code', 'depo_code']

    def to_json(self):
        return {
            "id": str(self.id),
            "depo": self.depo_code.to_json(),
            "market_code": self.market_code,
            "market_name": self.market_name,
            "price_code": str(self.price_code)
        }


class CustomerMaster(base_models.AuditModel):
    id = models.AutoField(primary_key=True, db_column='ID')
    customer_code = models.IntegerField(db_column='CUSTCODE', null=True, blank=True)
    sfa_temp_id = models.CharField(unique=True, max_length=50, db_column='TEMPID', null=True, blank=True)
    depo_code = models.ForeignKey(DepoMaster, db_column='DEPOCODE')
    actual_market_code = models.IntegerField(db_column='MKTCODE', null=True, blank=True)
    market_code = models.ForeignKey(Market, db_column='MKTCODEID', null=True, blank=True)
    customer_name = models.CharField(max_length=50, db_column='CUSTNAME')
    customer_add1 = models.CharField(max_length=55, db_column='CUSTADD1', null=True, blank=True)
    customer_add2 = models.CharField(max_length=55, db_column='CUSTADD2', null=True, blank=True)
    customer_city = models.CharField(max_length=35, db_column='CUSTCITY', null=True, blank=True)
    customer_pincode = models.CharField(db_column='CUSTPIN', max_length=10, null=True, blank=True)
    state_code = models.CharField(max_length=2, db_column='STATCODE', null=True, blank=True)
    customer_phonenumber = models.CharField(max_length=60, db_column='CUSTPHNO')
    customer_mail = models.CharField(max_length=35, db_column='CUSTMAIL', null=True, blank=True)
    mobile_phonenumber = models.CharField(max_length=20, db_column='MOBPHNO', null=True, blank=True)
    credit_days = models.IntegerField(db_column='CRDAYS', null=True, blank=True)
    credit_limit = models.IntegerField(db_column='CRLIMIT', null=True, blank=True)
    designation = models.CharField(max_length=25, db_column='DESIG', null=True, blank=True)
    mobile = models.CharField(max_length=25, db_column='MOBILE', null=True, blank=True)
    landline = models.CharField(max_length=25, db_column='LANDLINE', null=True, blank=True)
    mail = models.CharField(max_length=30, db_column='EMAIL', null=True, blank=True)
    short_name = models.CharField(max_length=12, db_column='SHORTNAME', null=True, blank=True)
    depot = models.IntegerField(db_column='DEPOT', null=True, blank=True)
    customer_id = models.IntegerField(db_column='CUSTID', null=True, blank=True)
    pan = models.CharField(max_length=15, db_column='PAN', null=True, blank=True)
    gstin = models.CharField(max_length=15, db_column='GSTIN', null=True, blank=True)

    def __str__(self):
        return "{} - {}".format(self.customer_code, self.depo_code)

    class Meta:
        verbose_name_plural = "Customer Master"
        db_table = "GCP_SM17_CUS"

    def to_json(self):
        return {
            "id": str(self.id),
            "customer_code": str(self.customer_code or ""),
            "sfa_temp_id": self.sfa_temp_id or "",
            "depo": self.depo_code.depo_code,
            "market": self.market_code.market_code if self.market_code else "",
            "customer_name": self.customer_name,
            "customer_add1": self.customer_add1 or "",
            "customer_add2": self.customer_add2 or "",
            "customer_city": self.customer_city or "",
            "customer_pincode": str(self.customer_pincode)  or "",
            "state_code": self.state_code or "",
            "customer_phonenumber": self.customer_phonenumber,
            "customer_mail": self.customer_mail or "",
            "mobile_phonenumber": self.mobile_phonenumber or "",
            "credit_days": str(self.credit_days or ""),
            "credit_limit": str(self.credit_limit or ""),
            "designation": self.designation or "",
            "mobile": self.mobile or "",
            "landline": self.landline or "",
            "mail": self.mail or "",
            "short_name": self.short_name or "",
            "depot": str(self.depot or ""),
            "customer_id": str(self.customer_id or ""),
            "pan": self.pan or "",
            "gstin": self.gstin or "",
            "is_sync": self.is_sync
        }


class DepoSalesRep(base_models.AuditModel):
    id = models.AutoField(primary_key=True, db_column='ID')
    code = models.CharField(max_length=3, db_column="CODE")
    depo_code = models.ForeignKey(DepoMaster, db_column='DEPOCODE')
    name = models.CharField(max_length=50, db_column="NAME")
    mobile = models.CharField(max_length=15, db_column="MOBILE")
    email_id = models.CharField(max_length=35, db_column="MAILID")
    active = models.BooleanField(default=True)

    def __str__(self):
        return "{}".format(self.code)

    class Meta:
        verbose_name_plural = "Depo Sales Representatives"
        db_table = "GCP_SM05_FLD"
        unique_together = ['code', 'depo_code']

    def to_json(self):
        return {
            "id": str(self.id),
            "depo": self.depo_code.to_json(),
            "dsr_code": self.code,
            "name": self.name,
            "mobile": self.mobile,
            "email": self.email_id,
            "active": self.active,
            "is_sync": self.is_sync
        }


class OrderHeader(base_models.AuditModel):
    id = models.AutoField(primary_key=True, db_column='ID')
    order_number = models.IntegerField(null=True, blank=True, db_column='OPNO')
    sfa_order_number = models.CharField(max_length=100, null=True, blank=True, db_column='SFAOPNO')
    order_date = models.DateField(db_column='OPDT')
    customer_code = models.ForeignKey(CustomerMaster, db_column='CUSTCODEID')
    customer = models.IntegerField(db_column='CUSTCODE', null=True, blank=True)
    depo_code = models.ForeignKey(DepoMaster, db_column='DEPOCODE')
    customer_reference_number = models.CharField(max_length=50, null=True, blank=True, db_column='CUSREFNO')
    customer_reference_date = models.DateField(null=True, blank=True, db_column='CUSREFDT')
    fs_code = models.CharField(null=True, blank=True, max_length=3, db_column='FSCODE')
    order_value = models.FloatField(db_column='ORDVAL')
    status = models.CharField(max_length=1, db_column='STATUS')
    order_created_date = models.DateField(db_column='CRETDATE')
    discount = models.FloatField(null=True, blank=True, db_column='DISCTOT')
    order_value_rs = models.FloatField(null=True, blank=True, db_column='ORDVALRS')
    shipped_date = models.DateField(null=True, blank=True, db_column='SHIPDT')

    def __str__(self):
        return "{}".format(self.order_number if self.order_number else self.sfa_order_number)

    class Meta:
        verbose_name_plural = "Order Header"
        db_table = "GCP_ST05_ORD_HDR"
        unique_together = ['order_number', 'sfa_order_number', 'order_date']

    def to_json(self, customer_detail=False, depo_detail=False):
        return {
            "id": str(self.id),
            "order_number": str(self.order_number or ""),
            "sfa_order_number": str(self.sfa_order_number or ""),
            "order_date": str(self.order_date),
            "customer": self.customer_code.to_json() if customer_detail
            else str(self.customer_code.customer_code or self.customer_code.sfa_temp_id),
            "depo": self.depo_code.to_json() if depo_detail
            else str(self.depo_code.depo_code),
            "customer_reference_number": self.customer_reference_number or "",
            "customer_reference_date": str(self.customer_reference_date or ""),
            "fs_code": self.fs_code or "",
            "order_value": str(self.order_value),
            "status": str(self.status),
            "order_created_date": str(self.order_created_date),
            "discount": str(self.discount or ""),
            "order_value_rs": str(self.order_value_rs or ""),
            "shipped_date": str(self.shipped_date or ""),
            "order_details": [each.to_json() for each in self.orderdetails_set.all()],
            "is_sync": self.is_sync
        }


class OrderDetails(base_models.AuditModel):
    id = models.AutoField(primary_key=True, db_column='ID')
    order = models.ForeignKey(OrderHeader, db_column='ORDID')
    order_number = models.IntegerField(null=True, blank=True, db_column='OPNO')
    order_date = models.DateField(db_column='OPDT')
    product_code = models.ForeignKey(ProductMaster, db_column='PRODCODE')
    order_quantity = models.IntegerField(db_column='ORDQTY')
    adjust_quantity = models.IntegerField(null=True, blank=True, db_column='ADJQTY')
    adjust_value = models.FloatField(null=True, blank=True, db_column='ADJVALUE')
    discount = models.FloatField(null=True, blank=True, db_column='DISCOUNT')
    all_quantity = models.IntegerField(null=True, blank=True, db_column='ALLQTY')
    sent_quantity = models.IntegerField(null=True, blank=True, db_column='SENTQTY')
    hold_quantity = models.IntegerField(null=True, blank=True, db_column='HOQTY')
    status = models.CharField(null=True, blank=True, max_length=1, db_column='STATUS')
    amount = models.FloatField(db_column='AMOUNT')
    order_created_date = models.DateField(null=True, blank=True, db_column='CRETDATE')
    order_detail_id = models.IntegerField(null=True, blank=True, db_column='OPDTLID')

    def __str__(self):
        return "{} - {}".format(self.order, self.product_code)

    class Meta:
        verbose_name_plural = "Order Details"
        db_table = "GCP_ST06_ORD_DTL"
        unique_together = ['order', 'product_code']

    def to_json(self, with_product=False):
        return {
            "id": str(self.id),
            "order_number": str(self.order_number or ""),
            "order_date": str(self.order_date),
            "product": self.product_code.to_json()
            if with_product else str(self.product_code.product_code),
            "order_quantity": str(self.order_quantity),
            "adjust_quantity": str(self.adjust_quantity or ""),
            "adjust_value": str(self.adjust_value or ""),
            "discount": str(self.discount or ""),
            "all_quantity": str(self.all_quantity or ""),
            "sent_quantity": str(self.sent_quantity or ""),
            "hold_quantity": str(self.hold_quantity or ""),
            "status": self.status or "",
            "amount": str(self.amount),
            "order_created_date": str(self.order_created_date or ""),
            "order_detail_id": str(self.order_detail_id or ""),
            "is_sync": self.is_sync
        }


class StockMaster(base_models.AuditModel):
    id = models.AutoField(primary_key=True, db_column='ID')
    product_code = models.ForeignKey(ProductMaster, db_column='PRODCODE')
    month = models.DateField(db_column='MONTH')
    depo_code = models.ForeignKey(DepoMaster, db_column='DEPOCODE')
    stock_flag = models.CharField(max_length=1, db_column='STKFLG')
    op_number = models.IntegerField(db_column='OPNO')
    op_date = models.DateField(db_column='OPDT')
    op_stock = models.IntegerField(db_column='OPSTK')
    quantity_received = models.IntegerField(db_column='QTYRECD')
    all_quantity = models.IntegerField(db_column='ALLQTY')
    clear_stock = models.IntegerField(db_column='CLSTK')
    free_stock = models.IntegerField(db_column='FREESTOCK')

    def __str__(self):
        return "{} - {} - {}".format(self.product_code, self.month, self.depo_code)

    class Meta:
        verbose_name_plural = "Stock Master"
        db_table = "GCP_WM01_STK_MAS"
        unique_together = ['product_code', 'month', 'depo_code',
                           'stock_flag', 'op_number', 'op_date']

    def to_json(self):
        return {
            "id": str(self.id),
            "product": str(self.product_code.product_code),
            "month": str(self.month),
            "depo": str(self.depo_code.depo_code),
            "stock_flag": self.stock_flag,
            "op_number": str(self.op_number),
            "op_date": str(self.op_date),
            "op_stock": str(self.op_stock),
            "quantity_received": str(self.quantity_received),
            "all_quantity": str(self.all_quantity),
            "clear_stock": str(self.clear_stock),
            "free_stock": str(self.free_stock)
        }


class InvoiceHeader(base_models.AuditModel):
    id = models.AutoField(primary_key=True, db_column='ID')
    invoice_number = models.CharField(db_column='INVNO', max_length=15)
    invoice_date = models.DateField(db_column='INVDT')
    invoice_type = models.CharField(max_length=1, db_column='INVTYPE')
    allocation_number = models.IntegerField(db_column='ALLOCNO')
    allocation_date = models.DateField(db_column='ALLOCDT')
    cancel = models.CharField(max_length=1, db_column='CANCEL', null=True, blank=True)
    depo_code = models.ForeignKey(DepoMaster, db_column='DEPOCODE')
    bank_code = models.CharField(max_length=50, db_column='BNKCODE', null=True, blank=True)
    bank_document_date = models.DateField(db_column='BNKDOCDT', null=True, blank=True)
    customer_code = models.ForeignKey(CustomerMaster, db_column='CUSTCODEID')
    customer = models.IntegerField(db_column='CUSTCODE', null=True, blank=True)
    balance_amount = models.FloatField(db_column='BALAMT', null=True, blank=True)
    total = models.FloatField(db_column='TOT', null=True, blank=True)
    total_discount = models.FloatField(db_column='TOT_DISC', null=True, blank=True)
    remarks = models.CharField(max_length=100, db_column='REMARKS', null=True, blank=True)
    roundoff = models.FloatField(db_column='ROUNDEDOFF')
    total_product_value = models.FloatField(db_column='TOT_PRODVAL')
    total_discount_value = models.FloatField(db_column='TOT_DISCOUNT')
    total_tax_value = models.FloatField(db_column='TOT_TAXABLE_VALUE')
    total_tax_amount = models.FloatField(db_column='TOT_TAXAMT', null=True, blank=True)
    net_amount = models.FloatField(db_column='NETAMT')
    advance_amount = models.FloatField(db_column='ADVAMT')
    credit_amount = models.FloatField(db_column='CRAMT')
    dr_amount = models.FloatField(db_column='DRAMT')
    paid_amount = models.FloatField(db_column='PAIDAMT', null=True, blank=True)
    invoice_amount = models.FloatField(db_column='INVAMT')
    other_charges = models.FloatField(db_column='OTHER_CHGS', null=True, blank=True)
    gross_weight = models.IntegerField(db_column='GROSSWT', null=True, blank=True)
    total_cgst_amount = models.FloatField(db_column='TOT_CGSTAMT')
    total_sgst_amount = models.FloatField(db_column='TOT_SGSTAMT')
    total_igst_amount = models.FloatField(db_column='TOT_IGSTAMT')
    invoice_gstin = models.CharField(max_length=15, db_column='INV_GSTIN', null=True, blank=True)

    def __str__(self):
        return "{}".format(self.invoice_number)

    class Meta:
        verbose_name_plural = "Invoice Header"
        db_table = "GCP_ST16_INV_HDR"

    def to_json(self):
        return {
            "id": str(self.id),
            "invoice_number": str(self.invoice_number),
            "invoice_date": str(self.invoice_date),
            "invoice_type": self.invoice_type,
            "allocation_number": str(self.allocation_number),
            "allocation_date": str(self.allocation_date),
            "cancel": self.cancel,
            "depo": str(self.depo_code.depo_code),
            "bank_code": str(self.bank_code),
            "bank_document_date": str(self.bank_document_date),
            "customer": str(self.customer_code.customer_code or self.customer_code.sfa_temp_id),
            "balance_amount": str(self.balance_amount),
            "total": str(self.total),
            "total_discount": str(self.total_discount),
            "remarks": self.remarks,
            "roundoff": str(self.roundoff),
            "total_product_value": str(self.total_product_value),
            "total_discount_value": str(self.total_discount_value),
            "total_tax_value": str(self.total_tax_value),
            "total_tax_amount": str(self.total_tax_amount),
            "net_amount": str(self.net_amount),
            "advance_amount": str(self.advance_amount),
            "credit_amount": str(self.credit_amount),
            "dr_amount": str(self.dr_amount),
            "paid_amount": str(self.paid_amount),
            "invoice_amount": str(self.invoice_amount),
            "other_charges": str(self.other_charges),
            "gross_weight": str(self.gross_weight),
            "total_cgst_amount": str(self.total_cgst_amount),
            "total_sgst_amount": str(self.total_sgst_amount),
            "total_igst_amount": str(self.total_igst_amount),
            "invoice_gstin": self.invoice_gstin,
            "invoice_details": [each.to_json() for each in self.invoicedetails_set.all()],
            "is_sync": self.is_sync
        }


class InvoiceDetails(base_models.AuditModel):
    id = models.AutoField(primary_key=True, db_column='ID')
    invoice_header = models.ForeignKey(InvoiceHeader, db_column='INVHDRID')
    product_code = models.ForeignKey(ProductMaster, db_column='PRODCODE')
    product_quantity = models.IntegerField(db_column='PRODQTY')
    product_rate = models.FloatField(db_column='PRODRATE')
    amount = models.FloatField(db_column='AMT')
    discount_percentage = models.FloatField(db_column='DISCPERC', null=True, blank=True)
    discount_amount = models.FloatField(db_column='DISCAMT', null=True, blank=True)
    tax_amount = models.FloatField(db_column='TAXAMT', null=True, blank=True)
    net_amount = models.FloatField(db_column='NETAMT', null=True, blank=True)
    ret_quantity = models.IntegerField(db_column='RETQTY')
    order = models.ForeignKey(OrderHeader, db_column='ORDID')
    order_number = models.IntegerField(db_column='ORDNO')
    order_date = models.DateField(db_column='ORDDT')
    total = models.FloatField(db_column='TOT', null=True, blank=True)
    cgst_per = models.FloatField(db_column='CGSTPER', null=True, blank=True)
    cgst_amount = models.FloatField(db_column='CGSTAMT')
    sgst_per = models.FloatField(db_column='SGSTPER', null=True, blank=True)
    sgst_amount = models.FloatField(db_column='SGSTAMT')
    igst_per = models.FloatField(db_column='IGSTPER', null=True, blank=True)
    igst_amount = models.FloatField(db_column='IGSTAMT')
    item_type = models.CharField(max_length=1, db_column='ITEMTYPE')
    tarrifid = models.ForeignKey(TariffMaster, db_column='TARIFFID')

    def __str__(self):
        return "{} - {}".format(self.invoice_header, self.product_code)

    class Meta:
        verbose_name_plural = "Invoice Details"
        db_table = "GCP_ST17_INV_DTL"

    def to_json(self):
        return {
            'id': str(self.id),
            'product_code': str(self.product_code.product_code),
            'product_quantity': str(self.product_quantity),
            'product_rate': str(self.product_rate),
            'amount': str(self.amount),
            'discount_percentage': str(self.discount_percentage),
            'discount_amount': str(self.discount_amount),
            'tax_amount': str(self.tax_amount),
            'net_amount': str(self.net_amount),
            'ret_quantity': str(self.ret_quantity),
            'order': {"order_number": str(self.order.order_number or ""),
                      "sfa_order_number": str(self.order.sfa_order_number or ""),
                      "order_date": str(self.order.order_date),},
            'order_number': str(self.order_number),
            'order_date': str(self.order_date),
            'total': str(self.total),
            'cgst_per': str(self.cgst_per),
            'cgst_amount': str(self.cgst_amount),
            'sgst_per': str(self.sgst_per),
            'sgst_amount': str(self.sgst_amount),
            'igst_per': str(self.igst_per),
            'igst_amount': str(self.igst_amount),
            'item_type': self.item_type,
            'tarrifid': str(self.tarrifid.tariff_id),
            "is_sync": self.is_sync
        }


class CollectionHeader(base_models.AuditModel):
    id = models.AutoField(primary_key=True, db_column='ID')
    sfa_receipt_id = models.IntegerField(null=True, blank=True, db_column='SFAID')
    depo_code = models.ForeignKey(DepoMaster, db_column='DEPOCODE')
    rmasid = models.IntegerField(null=True, blank=True, db_column='RMASID')
    sl_no = models.IntegerField(null=True, blank=True, db_column='SLNO')
    receipt_number = models.IntegerField(null=True, blank=True, db_column='RECPTNO')
    receipt_date = models.DateField(db_column='RECPTDT')
    m_receipt_number = models.IntegerField(null=True, blank=True, db_column='MRECPTNO')
    m_receipt_date = models.DateField(null=True, blank=True, db_column='MRECPTDT')
    voucher_type = models.CharField(null=True, blank=True, max_length=3, db_column='VOUTYPE')
    customer_code = models.ForeignKey(CustomerMaster, db_column='CUSTCODEID')
    customer = models.IntegerField(db_column='CUSTCODE', null=True, blank=True)
    pay_code = models.IntegerField(null=True, blank=True, db_column='PAYCODE')
    doc_number = models.CharField(null=True, blank=True, max_length=10, db_column='DOCNO')
    doc_date = models.DateField(null=True, blank=True, db_column='DOCDT')
    bank_name = models.CharField(null=True, blank=True, max_length=25, db_column='BANKNAME')
    br_name = models.CharField(null=True, blank=True, max_length=15, db_column='BRNAME')
    received_amount = models.FloatField(db_column='RECDAMT')
    advance_code = models.IntegerField(null=True, blank=True, db_column='ADVCODE')
    advance_amount = models.FloatField(null=True, blank=True, db_column='ADVAMT')
    bgl_code = models.IntegerField(null=True, blank=True, db_column='BGLCODE')
    bcgs_code = models.IntegerField(null=True, blank=True, db_column='BCGSCODE')
    bint_code = models.IntegerField(null=True, blank=True, db_column='BINTCODE')
    deposit_flag = models.IntegerField(null=True, blank=True, db_column='DEPOSITFLAG')
    bonus_flag = models.IntegerField(null=True, blank=True, db_column='BOUNSFLAG')
    round_plus = models.FloatField(null=True, blank=True, db_column='ROUNDPLUS')
    round_minus = models.FloatField(null=True, blank=True, db_column='ROUNDMINUS')
    c_flag = models.IntegerField(null=True, blank=True, db_column='CFLAG')
    cash_receipt_number = models.IntegerField(null=True, blank=True, db_column='CASH_RECEIPTNO')
    cash_receipt_date = models.DateField(null=True, blank=True, db_column='CASH_RECEIPTDT')
    remarks = models.CharField(null=True, blank=True, max_length=45, db_column='REMARKS')
    dis_receipt_number = models.IntegerField(null=True, blank=True, db_column='DIS_RECPTNO')
    place_supply = models.CharField(null=True, blank=True, max_length=30, db_column='PLACE_SUPPLY')
    courier_charges = models.FloatField(null=True, blank=True, db_column='COUR_CHARG')
    inter_state = models.CharField(null=True, blank=True, max_length=1, db_column='INTER_STAT')
    clearing_flag = models.IntegerField(null=True, blank=True, db_column='CLEARING_FLAG')

    def __str__(self):
        return "{} - {}".format(self.receipt_number
                                if self.receipt_number else self.sfa_receipt_id,
                                self.depo_code)

    class Meta:
        verbose_name_plural = "Collection Header"
        db_table = "GCP_FT71_RECEIPT_MAS"
        unique_together = ['depo_code', 'receipt_number', 'sfa_receipt_id']

    def to_json(self):
        return {
            'id': str(self.id),
            'sfa_receipt_id': str(self.sfa_receipt_id or ""),
            'depo_code': str(self.depo_code.depo_code),
            'rmasid': str(self.rmasid or ""),
            'sl_no': str(self.sl_no or ""),
            'receipt_number': str(self.receipt_number or ""),
            'receipt_date': str(self.receipt_date),
            'm_receipt_number': str(self.m_receipt_number or ""),
            'm_receipt_date': str(self.m_receipt_date or ""),
            'voucher_type': self.voucher_type or "",
            'customer_code': str(self.customer_code.customer_code),
            'pay_code': str(self.pay_code or ""),
            'doc_number': self.doc_number or "",
            'doc_date': str(self.doc_date or ""),
            'bank_name': self.bank_name or "",
            'br_name': self.br_name or "",
            'received_amount': str(self.received_amount),
            'advance_code': str(self.advance_code or ""),
            'advance_amount': str(self.advance_amount or ""),
            'bgl_code': str(self.bgl_code or ""),
            'bcgs_code': str(self.bcgs_code or ""),
            'bint_code': str(self.bint_code or ""),
            'deposit_flag': str(self.deposit_flag or ""),
            'bonus_flag': str(self.bonus_flag or ""),
            'round_plus': str(self.round_plus or ""),
            'round_minus': str(self.round_minus or ""),
            'c_flag': str(self.c_flag or ""),
            'cash_receipt_number': str(self.cash_receipt_number or ""),
            'cash_receipt_date': str(self.cash_receipt_date or ""),
            'remarks': self.remarks or "",
            'dis_receipt_number': str(self.dis_receipt_number or ""),
            'place_supply': self.place_supply or "",
            'courier_charges': str(self.courier_charges or ""),
            'inter_state': self.inter_state or "",
            'clearing_flag': str(self.clearing_flag or "")
        }


class CollectionDetails(base_models.AuditModel):
    id = models.AutoField(primary_key=True, db_column='ID')
    collection = models.ForeignKey(CollectionHeader, db_column='COLHDRID')
    depo_code = models.ForeignKey(DepoMaster, db_column='DEPOCODE')
    dtlid = models.IntegerField(null=True, blank=True, db_column='DTLID')
    rmasid = models.IntegerField(null=True, blank=True, db_column='RMASID')
    receipt_number = models.IntegerField(null=True, blank=True, db_column='RECPTNO')
    invoice_id = models.IntegerField(null=True, blank=True, db_column='INVID')
    gl_code = models.IntegerField(null=True, blank=True, db_column='GLCODE')
    bcgs = models.IntegerField(null=True, blank=True, db_column='BCGS')
    bint = models.IntegerField(null=True, blank=True, db_column='BINT')
    othamt = models.FloatField(null=True, blank=True, db_column='OTHAMT')
    received_amount = models.FloatField(null=True, blank=True, db_column='RECDAMT')
    invoice_code = models.ForeignKey(InvoiceHeader, null=True, blank=True, db_column='INVNO')
    tariff_id = models.ForeignKey(TariffMaster, null=True, blank=True, db_column='TARIFFID')
    cgst_per = models.FloatField(null=True, blank=True, db_column='CGSTPER')
    cgst_amount = models.FloatField(null=True, blank=True, db_column='CGSTAMT')
    sgst_per = models.FloatField(null=True, blank=True, db_column='SGSTPER')
    sgst_amount = models.FloatField(null=True, blank=True, db_column='SGSTAMT')
    igst_per = models.FloatField(null=True, blank=True, db_column='IGSTPER')
    igst_amount = models.FloatField(null=True, blank=True, db_column='IGST')
    total_tax_value = models.FloatField(null=True, blank=True, db_column='TAXABLE_VALUE')

    def __str__(self):
        return "{} - {}".format(self.collection, self.depo_code)

    class Meta:
        verbose_name_plural = "Collection Details"
        db_table = "GCP_FT72_RECEIPT_DTL"

    def to_json(self):
        return {
            'id': str(self.id),
            'depo_code': str(self.depo_code.depo_code),
            'dtlid': str(self.dtlid or ""),
            'rmasid': str(self.rmasid or ""),
            'receipt_number': str(self.receipt_number or ""),
            'invoice_id': str(self.invoice_id or ""),
            'gl_code': str(self.gl_code or ""),
            'bcgs': str(self.bcgs or ""),
            'bint': str(self.bint or ""),
            'othamt': str(self.othamt or ""),
            'received_amount': str(self.received_amount or ""),
            'invoice_code': str(self.invoice_code.id if self.invoice_code else ""),
            'order_code': str(self.order_code.id if self.order_code else ""),
            'tarif_id': str(self.tariff_id.tariff_id if self.tariff_id else ""),
            'cgst_per': str(self.cgst_per or ""),
            'cgst_amount': str(self.cgst_amount or ""),
            'sgst_per': str(self.sgst_per or ""),
            'sgst_amount': str(self.sgst_amount or ""),
            'igst_per': str(self.igst_per or ""),
            'igst_amount': str(self.igst_amount or ""),
            'total_tax_value': str(self.total_tax_value or "")
        }