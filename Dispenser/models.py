# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class DatiRaccolti(models.Model):

    date = models.DateTimeField(auto_now=True)
    erogation = models.BooleanField(default=False)
    userMod = models.BooleanField(default=False)  # flag erogazione utente/automatica
    timeMod = models.BooleanField(default=True)  # flag per distinguere giorno da notte. di default Giorno

    def __str__(self):
        return u'%s - %s - %s' % (self.date, self.erogation, self.userMod)

    class Meta:  # per evitare l'aggiunta della s finale al nome - specifico il plurale
        verbose_name_plural = "DatiRaccolti"


def __str__(self):
    return self.language.name

