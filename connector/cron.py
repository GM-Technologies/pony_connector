import json

import kronos
from datetime import datetime
from django.conf import settings
import requests
from django.db.models.query_utils import Q

from connector import sfa_urls
from connector.models import ProductMaster
from connector.utils import get_paginated_objects


@kronos.register('*/3 * * * *')
def data_sync():
    print "Initiating product sync"
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
    per_page = 1
    while not synced and len(unsynced_products):
        products, pagination_info = get_paginated_objects(unsynced_products, page, per_page)
        products = [each.to_json() for each in products]
        try:
            request_headers = {'Authorization': 'Token {}'.format(settings.SFA_TOKEN)}
            sync_product = requests.post(url=sfa_urls.PRODUCT_SYNC,
                                         data={'products': json.dumps(products)},
                                         headers=request_headers)
            print sync_product.status_code
        except:
            print "Failed"
        if pagination_info['has_next']():
            page = pagination_info['next_page_number']()
        else:
            synced = True
