from django.conf.urls import url, include
from django.contrib import admin
from Dispenser import views

urlpatterns = [

    url(r'^profile/', views.profile, name='profile'),

    url(r'^sensor/', views.sensor, name='sensor'),

    url(r'^client/', views.client, name='client'),  # get_post.html

    url(r'^dati/', views.sendData, name='dati'),  #chartInside.html, giorno da calendario
    url(r'^fake/', views.absentData, name='fake'),  # per controllare se i dati sono presenti o no

    url(r'^giorno/', views.ultimoDato, name='giorno'),  # per avere l'ultima riga -- aggiornamento

    # url(r'^periodo/', views.periodo, name='periodo'), ## RITORNA PAG PER VECCHIE STATISTICHE SETTIM/MENSILI. PRE INCONTRO FEDERICO
    url(r'^statistic/', views.periodo, name='statistic'),  ## RITORNA PG STATISTIC

    url(r'^fakeP/', views.absentDataPeriod, name='fakeP'),  ## RITORNA PG STATISTIC



    # da eliminare
    url(r'^erog/', views.invioErog, name='erog'),  # per ricevere i dati di erogazioni/passaggi

    url(r'^erogGN/', views.invioGiornoNotte, name='erog'),  # per ricevere i dati di erogazioni giorno/notte

]
