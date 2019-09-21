from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# -*- coding: utf-8 -*-

class Meal(models.Model):
    name      = models.CharField(max_length = 150)
    img_url   = models.URLField()
    category  = models.ForeignKey('Catergory')
    price     = models.FloatField()
    discount  = models.IntegerField()
    #restaurant = models.ManyToManyField('Restaurant', related_name = 'restaurants', blank=True)
    restaurant   = models.ForeignKey('Restaurant')
    rating       = models.IntegerField(default=5)
    delivery     = models.BooleanField(default=False)
    delivery_fee = models.IntegerField(blank=True)
    quantity     = models.IntegerField(blank=True)
    available   = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Catergory(models.Model):
    name       = models.CharField(max_length = 150)
    cat_type   = models.CharField(max_length = 150)
    restaurant = models.ForeignKey('Restaurant')
    
    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name      = models.CharField(max_length = 150)
    img_url   = models.URLField()
    rest_type = models.CharField(max_length = 150)
    phone_number = models.CharField(max_length = 20, default="08033334444")
    location  = models.CharField(max_length = 300)
    owner     = models.ForeignKey(User)
    opening_hours     = models.CharField(max_length = 100)
    closing_hours     = models.CharField(max_length = 100)
    rating            = models.IntegerField()
    delivery          = models.BooleanField(default=False)
    delivery_locations = models.CharField(max_length = 150, default="none")
    
    def __str__(self):
        return self.name

class Order(models.Model):
    order_detail = models.ManyToManyField('Order_Detail', related_name = 'order_detail', blank=True)
    restaurant   = models.ForeignKey('Restaurant')
    ref_number   = models.CharField(max_length = 100, default="no ref_number")
    status       = models.CharField(max_length = 300)
    name         = models.CharField(max_length = 100)
    address      = models.CharField(max_length = 350)
    phone        = models.CharField(max_length = 150)

    note         = models.CharField(max_length = 150)  
    
    def __str__(self):
        return str(self.restaurant.name)

class Order_Detail(models.Model):
    name           = models.CharField(max_length = 150)
    price          = models.FloatField()
    discount       = models.IntegerField()
    restaurant     = models.CharField(max_length = 150)
    status         = models.CharField(max_length = 150)
    quantity       = models.IntegerField()
    is_completed   = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Customer(models.Model):
    name      = models.CharField(max_length = 150)
    address   = models.CharField(max_length = 150)
    
    def __str__(self):
        return self.name