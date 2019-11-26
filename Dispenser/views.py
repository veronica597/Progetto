# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, Http404
from .models import DatiRaccolti
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from django.http import JsonResponse
from django.utils import timezone
from django.db import models


@csrf_exempt
def index(request):
    # return HttpResponse("<p> Food Dispenser Application </p>")
    return render(request, 'home.html')


def profile(request):
    return HttpResponse("<p>Profile page of user </p>")


@csrf_exempt
def sensor(request):  # processa i dati da inserire nel database

    if request.method == 'POST':
        print('post')
        print(request.body)
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)  # e' un dict python

        sensor_data = DatiRaccolti()

        sensor_data.erogation = body_data['erogation']
        sensor_data.userMod = body_data['userMod']
        sensor_data.timeMod = body_data['timeMod']

        sensor_data.save()

        return HttpResponse()

    return HttpResponseForbidden


@csrf_exempt
def client(request):  # processa i dati inviati a seguito del click dell'utente

    if request.method == 'POST':  # RIGUARDARE
        print('post')
        print(request.body)
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)  # e' un oggetto python

        sensor_data = DatiRaccolti()

        sensor_data.erogation = body_data['erogation']
        sensor_data.userMod = body_data['userMod']
        sensor_data.timeMod = body_data['timeMod']

        sensor_data.save()

        return HttpResponse()

    if request.method == 'GET':
        print('get')
        oggi = datetime.date.today()
        print(oggi)
        context = {
            'righe': DatiRaccolti.objects.values().filter(date=oggi),
        }

        return render(request, 'get_post.html', context)

    return HttpResponseForbidden


@csrf_exempt
def grafico(request):  # inserire la parte per interpretare request.GET
    # quando clicco invio dei parametri che qui vengono recuperati per fitrare i dati-->  invio il context
    context = {'righe': DatiRaccolti.objects.values().filter(date__gte="2019-10-22")}  # dati del giorno corrente
    return render(request, 'chartInside.html', context)


@csrf_exempt
def sendData(request):  # view che invia i dati per costruire il CHART erogazioni utente/automatiche lato html

    anno = request.GET.__getitem__('anno')
    mese = request.GET.__getitem__('mese')
    giorno = request.GET.__getitem__('giorno')
    stringa = anno + "-" + mese + "-" + giorno
    print(stringa)

    eA = DatiRaccolti.objects.values('date').filter(date__gte=stringa, erogation=True, userMod=False).order_by('date').count()
    eU = DatiRaccolti.objects.values('date').filter(date__gte=stringa, erogation=True, userMod=True).order_by('date').count()

    # dovro' mettere tipo date__day = giorno, date__month = mese , ...

    print("eA: " + str(eA))
    print("eU: " + str(eU))

    erogazioni = [stringa, eA, eU]
    return JsonResponse(erogazioni, safe=False)

    # context = {'giorno': stringa, 'erogA': eA, 'erogU': eU}
    # return render(request, 'chartInside.html', context)


@csrf_exempt
def ultimoDato(request):  # per aggiornamento tabella e chart
    anno = request.GET.__getitem__('anno')
    mese = request.GET.__getitem__('mese')
    giorno = request.GET.__getitem__('giorno')
    stringa = anno + "-" + mese + "-" + giorno
    print(stringa)
    elementi = DatiRaccolti.objects.values().filter(date__gte=stringa)

    # .strftime("%b. %d, %Y, %H:%M %p"))  # :%f per i millisecondi

    lu = len(elementi)
    print(lu)
    if lu == 0:  # il database non contiene dati per il giorno corrente
        f = "Non ci sono erogazioni per il giorno corrente"

    else:
        f = elementi[lu - 1]  # invio sempre l'ultimo elemento

    print(f)

    return JsonResponse(f, safe=False)


@csrf_exempt
def periodo(request):  # per filtraggio mese/settimana
    annoI = request.GET.__getitem__('annoI')
    meseI = request.GET.__getitem__('meseI')
    giornoI = request.GET.__getitem__('giornoI')

    stringaI = annoI + "-" + meseI + "-" + giornoI

    annoF = request.GET.__getitem__('annoF')
    meseF = request.GET.__getitem__('meseF')
    giornoF = request.GET.__getitem__('giornoF')

    stringaF = annoF + "-" + meseF + "-" + giornoF

    # per grafico stile giorno singolo --> ho due colonne una per le erogazioni automatiche e una per le erogazioni utente

    eA = DatiRaccolti.objects.values('date').filter(date__gte=stringaI, date__lte=stringaF, erogation=True, userMod=False).order_by('date').count()
    # primo compreso, ultimo escluso --mi va bene ?
    # anche utilizzando date__range=[..] ottengo lo stesso risultato
    eU = DatiRaccolti.objects.values('date').filter(date__gte=stringaI, date__lte=stringaF, erogation=True, userMod=True).order_by('date').count()

    print("eA: " + str(eA))
    print("eU: " + str(eU))

    erogazioni = [eA, eU]  # come categories cosa passo ??
    return JsonResponse(erogazioni, safe=False)

    # context = {'giorno': stringa, 'erogA': eA, 'erogU': eU}
    # return render(request, 'chartInside.html', context)


@csrf_exempt
def grafico_periodo(request):

    # mettere context
    # context = {'righe': DatiRaccolti.objects.values('date').filter(date__gte=stringaI, date__lte=stringaF, erogation=True, userMod=False).order_by('date')}
    return render(request, 'periodo.html')


@csrf_exempt
def invioErog(request):  # views per grafico erogazioni/passaggi
    anno = request.GET.__getitem__('anno')
    mese = request.GET.__getitem__('mese')
    giorno = request.GET.__getitem__('giorno')
    stringa = anno + "-" + mese + "-" + giorno
    print(stringa)

    e = DatiRaccolti.objects.values('date').filter(date__gte=stringa, erogation=True).order_by('date').count()
    noE = DatiRaccolti.objects.values('date').filter(date__gte=stringa, erogation=False).order_by('date').count()

    # dovro' mettere tipo date__day = giorno, date__month = mese , ...

    print("e: " + str(e))
    print("noE: " + str(noE))

    erogazioni = [stringa, e, noE]
    return JsonResponse(erogazioni, safe=False)

    # context = {'giorno': stringa, 'erogA': eA, 'erogU': eU}
    # return render(request, 'chartInside.html', context)

# views per grafico erogazioni giorno/notte


@csrf_exempt
def invioGiornoNotte(request):
    anno = request.GET.__getitem__('anno')
    mese = request.GET.__getitem__('mese')
    giorno = request.GET.__getitem__('giorno')
    stringa = anno + "-" + mese + "-" + giorno
    print(stringa)

    eG = DatiRaccolti.objects.values('date').filter(date__gte=stringa, erogation=True, timeMod=True).order_by('date').count()  # giorno
    eN = DatiRaccolti.objects.values('date').filter(date__gte=stringa, erogation=True, timeMod=False).order_by('date').count()  # notte

    # dovro' mettere tipo date__day = giorno, date__month = mese , ...

    print("eG: " + str(eG))
    print("eN: " + str(eN))

    erogazioni = [stringa, eG, eN]
    return JsonResponse(erogazioni, safe=False)

    # context = {'giorno': stringa, 'erogA': eA, 'erogU': eU}
    # return render(request, 'chartInside.html', context)

