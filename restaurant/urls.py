from django.conf.urls import url
from .views import *


urlpatterns = [
	url(r'^$', index, name='index'),
	url(r'^order/$', order, name='order'),
	url(r'^order/list/$', order_list, name='order_list'),
]
