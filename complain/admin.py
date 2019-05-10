# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Govt_Agency, Complain, Govt_Agency_Access, Complain_i

admin.site.register(Govt_Agency)
admin.site.register(Complain)
admin.site.register(Govt_Agency_Access)
admin.site.register(Complain_i)
