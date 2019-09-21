from django.conf.urls import url
from django.contrib import admin

from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token


from .views import (
    UserCreateAPIView,
    UserLoginAPIView,
    MealAPIView,
    MealList,
    MealDetail,
    RestaurantDetail,
    RestaurantList,
    OrderDetail,
    OrderList,
    OrderrList,

    PostListAPIView,
    saveOrder,

    CustomAuthToken,
    setMealAvailability
    )

urlpatterns = [
    url(r'^login/$', UserLoginAPIView.as_view(), name='login'),
    #url(r'^register/$', UserCreateAPIView.as_view(), name='register'),
    url(r'^auth/token/', CustomAuthToken.as_view()),#obtain_jwt_token),
    url(r'^auth/token/refresh/', refresh_jwt_token),
    #url(r'^meals/<pk>/$', MealDetail.as_view(), name='meals-detial'),
    url(r'^meal/(?P<pk>\d+)/$', MealDetail.as_view(), name='meals-detial'),
    url(r'^meals/all/$', MealList.as_view(), name='meals-list'),
    url(r'^meals/$', PostListAPIView.as_view(), name='meals-list'),
    url(r'^meal/available/(?P<pk>\d+)/$', setMealAvailability, name='meals-list'),

    url(r'^restaurant/(?P<pk>\d+)/$', RestaurantDetail.as_view(), name='meals-detial'),
    url(r'^restaurant/$', RestaurantList.as_view(), name='meals-list'),

    url(r'^order/(?P<pk>\d+)/$', OrderDetail.as_view(), name='order-detial'),
    url(r'^order/$', OrderrList.as_view(), name='order-list'),

    url(r'^place/order/$', saveOrder, name='order-list'),
    
]
