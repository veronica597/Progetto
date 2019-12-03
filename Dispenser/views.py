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
from django.db.models import Q


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

    if request.method == 'GET':

        print('get')
        oggi = datetime.date.today()
        e = DatiRaccolti.objects.values('date').filter(date__gte=oggi, erogation=True).order_by('date').count()
        noE = DatiRaccolti.objects.values('date').filter(date__gte=oggi, erogation=False).order_by('date').count()

        print("e: " + str(e))
        print("noE: " + str(noE))

        context = {
            'erog': e,
            'noErog': noE,
            'righe': DatiRaccolti.objects.values().filter(date__gte=oggi)
        }

        return render(request, 'get_post.html', context)

    return HttpResponseForbidden


@csrf_exempt
def sendData(request):  # view che invia i dati per costruire il CHART erogazioni utente/automatiche lato html

    # anno = request.GET.__getitem__('anno')
    # mese = request.GET.__getitem__('mese')
    # giorno = request.GET.__getitem__('giorno')
    anno = request.GET.get('anno')
    mese = request.GET.get('mese')
    giorno = request.GET.get('giorno')
    stringa = anno + "-" + mese + "-" + giorno
    stringaI = giorno + "-" + mese + "-" + anno  # per categories grafico
    print(stringa)

    # d = datetime.datetime(int(anno), int(mese), int(giorno), 0, 0, 0, tzinfo)
    # print(d)

    eA = DatiRaccolti.objects.values('date').filter(date__contains=stringa, erogation=True, userMod=False).order_by('date').count()
    eU = DatiRaccolti.objects.values('date').filter(date__contains=stringa, erogation=True, userMod=True).order_by('date').count()

    e = DatiRaccolti.objects.values('date').filter(date__contains=stringa, erogation=True).order_by('date').count()  # erogazioni
    noE = DatiRaccolti.objects.values('date').filter(date__contains=stringa, erogation=False).order_by('date').count()  # no erogazioni

    eG = DatiRaccolti.objects.values('date').filter(date__contains=stringa, erogation=True, timeMod=True).order_by('date').count()  # giorno
    eN = DatiRaccolti.objects.values('date').filter(date__contains=stringa, erogation=True, timeMod=False).order_by('date').count()  # notte

    print("eA: " + str(eA))
    print("eU: " + str(eU))

    print("e: " + str(e))
    print("noE: " + str(noE))

    print("eG: " + str(eG))
    print("eN: " + str(eN))

    # i = Q(date__lte=stringa)
    # f = Q(date__gte=stringa)
    #
    # # p = DatiRaccolti.objects.values().filter(date__gte=stringa).get(pk=1)
    # # print(p)

    context = {'righe': DatiRaccolti.objects.values().filter(date__startswith=stringa).order_by('date'),  # sistemare contains
               'giorno': json.dumps(stringaI), 'erogA': eA, 'erogU': eU, 'erog': e, 'noErog': noE, 'erogG': eG, 'erogN': eN}

    return render(request, 'chartInside.html', context)


@csrf_exempt
def absentData(request):
    anno = request.GET.__getitem__('anno')
    mese = request.GET.__getitem__('mese')
    giorno = request.GET.__getitem__('giorno')
    stringa = anno + "-" + mese + "-" + giorno
    print(stringa)

    f = DatiRaccolti.objects.values().filter(date__contains=stringa).order_by('date')  # sistemare contains
    lu = len(f)

    return JsonResponse(lu, safe=False)


@csrf_exempt
def ultimoDato(request):  # per aggiornamento tabella e chart

    stringa = datetime.date.today()
    elementi = DatiRaccolti.objects.values().filter(date__gte=stringa)

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

    id = request.GET.__getitem__('id')
    print('id: ' + id)

    # oggi = datetime.date.today()
    oggi = datetime.date(2019, 10, 22)

    meseC = oggi.month
    giornoC = oggi.day
    annoC = oggi.year

    print("oggi: " + str(oggi))

    # in base al valore dell'id passato calcolo giorno mese scorso o giorno settimana scorsa

    if id == '1':  # mese
        print("mesee")
        giornoP = giornoC  # mantengo il giorno

        if meseC == 1:  # se e' gennaio cambio il mese ma anche l'anno
            meseP = 12
            annoP = annoC - 1

        else:
            meseP = meseC - 1
            annoP = annoC

        passato = datetime.date(annoP, meseP, giornoP)

    elif id == '0':  # settimana
        print("settimana")
        mesi31 = [3, 5, 8, 10]
        mesi30 = [0, 2, 4, 6, 7, 9, 11]

        if giornoC <= 7:
            annoP = annoC
            meseP = meseC - 1

            if meseC == 1:
                annoP = annoC - 1

            if meseP in mesi31:
                giornoP = 31 + (giornoC - 7)

            elif meseP in mesi30:
                giornoP = 30 + (giornoC - 7)

            elif meseP == 2:
                giornoP = 28 + (giornoC - 7)

        else:
            meseP = meseC  # mantengo il mese
            giornoP = giornoC - 7
            annoP = annoC

        passato = datetime.date(annoP, meseP, giornoP)

    print(passato)

    inizio = str(giornoP) + "-" + str(meseP) + "-" + str(annoP)
    fine = str(giornoC) + "-" + str(meseC) + "-" + str(annoC)

    eA = DatiRaccolti.objects.values('date').filter(date__gte=passato, date__lte=oggi, erogation=True, userMod=False).order_by('date').count()
    eU = DatiRaccolti.objects.values('date').filter(date__gte=passato, date__lte=oggi, erogation=True, userMod=True).order_by('date').count()

    e = DatiRaccolti.objects.values('date').filter(date__gte=passato, date__lte=oggi, erogation=True).order_by('date').count()  # erogazioni
    noE = DatiRaccolti.objects.values('date').filter(date__gte=passato, date__lte=oggi, erogation=False).order_by('date').count()  # no erogazioni

    eG = DatiRaccolti.objects.values('date').filter(date__gte=passato, date__lte=oggi, erogation=True, timeMod=True).order_by('date').count()  # giorno
    eN = DatiRaccolti.objects.values('date').filter(date__gte=passato, date__lte=oggi, erogation=True, timeMod=False).order_by('date').count()  # notte

    print("eA: " + str(eA))
    print("eU: " + str(eU))

    print("e: " + str(e))
    print("noE: " + str(noE))

    print("eG: " + str(eG))
    print("eN: " + str(eN))

    context = {'erogA': eA, 'erogU': eU, 'erog': e, 'noErog': noE, 'erogG': eG, 'erogN': eN, 'inizio': json.dumps(inizio), 'fine': json.dumps(fine),
               'righe': DatiRaccolti.objects.values().filter(date__gte=passato, date__lte=oggi, erogation=True, userMod=False).order_by('date')}
    return render(request, 'periodo.html', context)


# Da eliminare
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

