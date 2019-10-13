from django.conf.urls import url, include
from django.contrib import admin
from Dispenser import views

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    # url(r'', include('Dispenser.urls')),
    url(r'^$', views.home, name='home'),
    url(r'^sensor/', views.sensor, name='sensor'),
    # url(r'^admin/', admin.site.urls),
    url(r'^client/', views.client, name='client'),

]
