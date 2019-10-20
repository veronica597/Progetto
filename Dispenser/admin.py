# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from . import models


class DatiAdmin(admin.ModelAdmin):
    list_display = ('date','erogation','userMod','timeMod')
    ordering = ['date']
    list_filter = ['date','erogation','userMod','timeMod']


admin.site.register(models.DatiRaccolti,DatiAdmin)
