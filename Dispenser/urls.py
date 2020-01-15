
from django.conf.urls import url
from Dispenser import views

urlpatterns = [

    url(r'^sensor/', views.sensor, name='sensor'),

    url(r'^client/', views.client, name='client'),  # get_post.html

    url(r'^dati/', views.sendData, name='dati'),  # chartInside.html, giorno da calendario
    url(r'^fake/', views.absentData, name='fake'),  # per controllare se i dati sono presenti o no

    url(r'^giorno/', views.ultimoDato, name='giorno'),  # per avere l'ultima riga -- aggiornamento

    url(r'^statistic/', views.periodo, name='statistic'),  ## RITORNA PG STATISTIC

    url(r'^fakeP/', views.absentDataPeriod, name='fakeP'),  ## RITORNA PG STATISTIC

    url(r'^fakeSM/', views.absentDataSM, name='fakeSM'),  # per verificare se ci sono dati per la settimana/il mese piu' recente

]
