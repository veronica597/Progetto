
from django.conf.urls import url
from Dispenser import views

urlpatterns = [

    url(r'^sensor/', views.sensor, name='sensor'),

    url(r'^client/', views.client, name='client'),  # getPost.html

    url(r'^data/', views.sendData, name='data'),  # chartInside.html, giorno da calendario
    url(r'^fake/', views.absentData, name='fake'),  # per controllare se i dati sono presenti o no

    url(r'^day/', views.LastAdded, name='day'),  # per avere l'ultima riga -- aggiornamento

    url(r'^statistic/', views.Period, name='statistic'),  ## RITORNA PG STATISTIC

    url(r'^fakeP/', views.absentDataPeriod, name='fakeP'),  ## RITORNA PG STATISTIC

    url(r'^fakeWM/', views.absentDataWM, name='fakeWM'),  # per verificare se ci sono dati per la settimana/il mese piu' recente

]
