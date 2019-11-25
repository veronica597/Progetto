from django.conf.urls import url, include
from django.contrib import admin
from Dispenser import views
from django.views.generic import TemplateView

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    # url(r'', include('Dispenser.urls')),
    url(r'^$', views.home, name='home'),

    url(r'^sensor/', views.sensor, name='sensor'),
    # url(r'^admin/', admin.site.urls),
    url(r'^client/', views.client, name='client'),  # get_post.html

    # url(r'^ajax/', views.ajax, name='ajax'),
    # url(r'^visual/', views.visual, name='visual'),

    url(r'^gajax/', views.get_ajax, name='gajax'),

    # url(r'^$', views.viewData, name='viewData'),  # /dispenser --> dati tabella. VIEW CHIARA

    # url(r'^chart/', views.chartData, name='chart'),
    url(r'^aggiornamento/', views.LastDate, name='agg'),

    url(r'^chart/', views.grafico, name='grafico'),
    url(r'^dati/', views.sendData, name='dati'),

    url(r'^giorno/', views.ultimoDato, name='giorno'),
    url(r'^periodo/', views.periodo, name='periodo'),
    url(r'^grafPeriodo/', views.grafico_periodo, name='grafP'),






]
