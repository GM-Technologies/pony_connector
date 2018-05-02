from django.conf.urls import url

from connector.views import index

urlpatterns = [
    url(r'^$', index, name='index'),
]