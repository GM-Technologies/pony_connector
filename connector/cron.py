import kronos
from django.db.models.query_utils import Q

from connector.models import ProductMaster


@kronos.register('*/3 * * * *')
def data_sync():
    print "Initiating product sync"
    unsynced_products = ProductMaster.objects.filter(Q(Q(is_sync=False) |
                                                       Q(category__is_sync=False) |
                                                       Q(sub_category__is_sync=False))
                                                     ).distinct()

    print unsynced_products[0].to_json()
