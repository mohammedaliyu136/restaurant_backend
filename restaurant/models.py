from __future__ import unicode_literals

from django.db import models

# Create your models here.
# -*- coding: utf-8 -*-

class Meal(models.Model):
    name      = models.CharField(max_length = 150)
    img       = models.ImageField('/img')
    category  = models.ForeignKey('Catergory')
    price     = models.FloatField()
    discount  = models.IntegerField()
    #restaurant = models.ManyToManyField('Restaurant', related_name = 'restaurants', blank=True)
    restaurant = models.ForeignKey('Restaurant')

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
    rest_type = models.CharField(max_length = 150)
    location  = models.CharField(max_length = 300)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    meal = models.ManyToManyField('Meal', related_name = 'meals', blank=True)
    restaurant  = models.ForeignKey('Restaurant')
    customer  = models.ForeignKey('Customer')
    status  = models.CharField(max_length = 300)
    
    def __str__(self):
        return str(self.customer.name)+' - '+str(self.meal.all()[0])


class Customer(models.Model):
    name      = models.CharField(max_length = 150)
    address = models.CharField(max_length = 150)
    
    def __str__(self):
        return self.name