# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class DatiRaccolti(models.Model):

    date = models.DateTimeField(auto_now=True)
    erogation= models.BooleanField(default=False)
    userMod= models.BooleanField(default=False)

def __str__(self):
    return self.language.name
