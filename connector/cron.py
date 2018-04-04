import json

import kronos
from datetime import datetime
from django.conf import settings
import requests
from django.db.models.query_utils import Q

from connector import sfa_urls
from connector.models import ProductMaster, DivisionMaster, DepoMaster, CustomerMaster
from connector.utils import get_paginated_objects


@kronos.register('*/5 * * * *')
def data_sync():
    print "Product sync initiated at {}".format(datetime.now())
    product_sync()
    print "Product sync completed at {}".format(datetime.now())
    print "Division sync initiated at {}".format(datetime.now())
    division_sync()
    print "Division sync completed at {}".format(datetime.now())
    print "Depo sync initiated at {}".format(datetime.now())
    depo_sync()
    print "Depo sync completed at {}".format(datetime.now())
    print "Customer sync initiated at {}".format(datetime.now())
    customer_sync()
    print "Customer sync completed at {}".format(datetime.now())


def product_sync():
    unsynced_products = list(ProductMaster.objects.filter(
        Q(Q(Q(is_sync=False) |
            Q(category__is_sync=False) |
            Q(sub_category__is_sync=False) |
            Q(Q(price__with_effect_from__lte=datetime.now().date()) & Q(price__is_sync=False))
            ) & Q(price__isnull=False))
    ).distinct().select_related('category',
                                'sub_category',
                                'tariff'))
    synced = False
    page = 1
    per_page = 50
    while not synced and len(unsynced_products):
        products, pagination_info = get_paginated_objects(unsynced_products, page, per_page)
        product_data = [each.to_json() for each in products]
        try:
            request_headers = {'Authorization': 'Token {}'.format(settings.SFA_TOKEN)}
            sync_product = requests.post(url=sfa_urls.PRODUCT_SYNC,
                                         data={'products': json.dumps(product_data)},
                                         headers=request_headers)
            response = json.loads(sync_product.content)
            for each in response:
                if not each:
                    continue
                try:
                    product = ProductMaster.objects.get(product_code=each['product_code'])
                    product.is_sync = each['is_sync']
                    product.save(update_fields=['is_sync'])
                    category = product.category
                    category.is_sync = each['is_sync']
                    category.save(update_fields=['is_sync'])
                    sub_category = product.sub_category
                    sub_category.is_sync = each['is_sync']
                    sub_category.save(update_fields=['is_sync'])
                    price = product.price_set.all().get(id=each['price'].get('id'))
                    price.is_sync = each['is_sync']
                    price.save(update_fields=['is_sync'])
                except BaseException as ex:
                    print ex
        except BaseException as ex:
            print ex
        if pagination_info['has_next']():
            page = pagination_info['next_page_number']()
        else:
            synced = True


def division_sync():
    unsynced_divisions = list(DivisionMaster.objects.filter(is_sync=False))
    synced = False
    page = 1
    per_page = 50
    while not synced and len(unsynced_divisions):
        divisions, pagination_info = get_paginated_objects(unsynced_divisions, page, per_page)
        division_data = [each.to_json() for each in divisions]
        try:
            request_headers = {'Authorization': 'Token {}'.format(settings.SFA_TOKEN)}
            sync_division = requests.post(url=sfa_urls.DIVISION_SYNC,
                                         data={'divisions': json.dumps(division_data)},
                                         headers=request_headers)
            if not sync_division.status_code == 200:
                raise Exception('{} response from SFA'.format(sync_division.status_code))
            response = json.loads(sync_division.content)
            for each in response:
                if not each:
                    continue
                try:
                    division = DivisionMaster.objects.get(division_code=each['division_code'])
                    division.is_sync = each['is_sync']
                    division.save(update_fields=['is_sync'])
                except BaseException as ex:
                    print ex
        except BaseException as ex:
            print ex
        if pagination_info['has_next']():
            page = pagination_info['next_page_number']()
        else:
            synced = True


def depo_sync():
    unsynced_depos = list(DepoMaster.objects.filter(is_sync=False))
    synced = False
    page = 1
    per_page = 50
    while not synced and len(unsynced_depos):
        depos, pagination_info = get_paginated_objects(unsynced_depos, page, per_page)
        depo_data = [each.to_json() for each in depos]
        try:
            request_headers = {'Authorization': 'Token {}'.format(settings.SFA_TOKEN)}
            sync_depo = requests.post(url=sfa_urls.DEPO_SYNC,
                                         data={'depos': json.dumps(depo_data)},
                                         headers=request_headers)
            if not sync_depo.status_code == 200:
                raise Exception('{} response from SFA'.format(sync_depo.status_code))
            response = json.loads(sync_depo.content)
            for each in response:
                if not each:
                    continue
                try:
                    depo = DepoMaster.objects.get(depo_code=each['depo_code'])
                    depo.is_sync = each['is_sync']
                    depo.save(update_fields=['is_sync'])
                except BaseException as ex:
                    print ex
        except BaseException as ex:
            print ex
        if pagination_info['has_next']():
            page = pagination_info['next_page_number']()
        else:
            synced = True


def customer_sync():
    unsynced_customers = list(CustomerMaster.objects.filter(customer_code__isnull=False,
                                                            is_sync=False))
    synced = False
    page = 1
    per_page = 50
    while not synced and len(unsynced_customers):
        customers, pagination_info = get_paginated_objects(unsynced_customers, page, per_page)
        customer_data = [each.to_json() for each in customers]
        try:
            request_headers = {'Authorization': 'Token {}'.format(settings.SFA_TOKEN)}
            sync_customer = requests.post(url=sfa_urls.CUSTOMER_SYNC,
                                         data={'customers': json.dumps(customer_data)},
                                         headers=request_headers)
            if not sync_customer.status_code == 200:
                raise Exception('{} response from SFA'.format(sync_customer.status_code))
            response = json.loads(sync_customer.content)
            for each in response:
                if not each:
                    continue
                try:
                    customer = CustomerMaster.objects.get(id=each['id'])
                    customer.is_sync = each['is_sync']
                    customer.save(update_fields=['is_sync'])
                except BaseException as ex:
                    print ex
        except BaseException as ex:
            print ex
        if pagination_info['has_next']():
            page = pagination_info['next_page_number']()
        else:
            synced = True