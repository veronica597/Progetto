from django.conf.urls import url, include
from django.contrib import admin
from Dispenser import views

urlpatterns = [

    url(r'^profile/',views.profile, name='profile'),


    url(r'^sensor/', views.sensor, name='sensor'),

    url(r'^client/', views.client, name='client'),  # get_post.html

    url(r'^chart/', views.grafico, name='grafico'),  # giorno qualunque NO giorno corrente
    url(r'^dati/', views.sendData, name='dati'),  # per ricevere i dati di erogazioni automatiche/utente

    url(r'^giorno/', views.ultimoDato, name='giorno'),  # per avere l'ultima riga -- aggiornamento

    url(r'^periodo/', views.periodo, name='periodo'),
    url(r'^grafPeriodo/', views.grafico_periodo, name='grafP'),

    url(r'^erog/', views.invioErog, name='erog'),  # per ricevere i dati di erogazioni/passaggi

    url(r'^erogGN/', views.invioGiornoNotte, name='erog'),  # per ricevere i dati di erogazioni giorno/notte


]
