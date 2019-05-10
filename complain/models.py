# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Govt_Agency(models.Model):
    name = models.CharField(max_length=45)
    department = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=30)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.name, self.department)

class Complain(models.Model):
    code = models.CharField(max_length=10)
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=1000)
    status = models.CharField(max_length=10, default='not read')
    govt_agency = models.ForeignKey(Govt_Agency)

    def __str__(self):
        return self.subject

class Govt_Agency_Access(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    agency = models.OneToOneField(Govt_Agency, default='normal')

    def __str__(self):
        return "%s %s" % (self.user.username, self.agency)


class Complain_i(models.Model):
    title = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=500, blank=True)
    document = models.FileField(upload_to='documents/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)