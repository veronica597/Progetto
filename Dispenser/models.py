# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone

from django.db import models


class DatiRaccolti(models.Model):

    date = models.DateTimeField(auto_now=True)
    # date = models.DateTimeField(default=timezone.now(), blank=True)
    erogation = models.BooleanField(default=False)
    userMod = models.BooleanField(default=False)  # flag erogazione utente/automatica
    timeMod = models.BooleanField(default=True)  # flag per distinguere giorno da notte. di default Giorno

    def __str__(self):
        # stringa = "{} {} {} {}"
        # stringa.format(str(self.date), str(self.erogation), str(self.userMod), str(self.timeMod))
        # return stringa
        # return u'%s' % stringa
        return u'%s  %s  %s  %s' % (self.date, self.erogation, self.userMod,  self.timeMod)

    class Meta:  # per evitare l'aggiunta della s finale al nome - specifico il plurale
        verbose_name_plural = "DatiRaccolti"


def __str__(self):
    return self.language.name


 # def getDate(self):
 #     return self.date.strftime('%Y-%m-%d%H')

