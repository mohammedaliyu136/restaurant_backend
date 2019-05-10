from django.conf.urls import url
from .views import *
from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
	url(r'^$', index, name='index'),

]
