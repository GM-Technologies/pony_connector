# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse


def index(request):
    text = '<div style="position: fixed; display: flex; align-items: center; top: 0;' \
           ' font-family: \'Helvetica Neue\',Helvetica,Arial,sans-serif; left: 0; width: ' \
           '100%; height: 100%; background-color: white; text-align: center; z-index: ' \
           '1000000;"><h4 style="width:100%">Gladminds Administration<br>Permission ' \
           'denied</h4></div>'
    return HttpResponse(text)
