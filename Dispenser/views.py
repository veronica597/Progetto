# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, Http404
from .models import DatiRaccolti
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from datetime import datetime
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
        # oggi = datetime.date.today()
        oggi = datetime.today()
        e = DatiRaccolti.objects.values('date').filter(date__gte=oggi, erogation=True).order_by('date').count()
        noE = DatiRaccolti.objects.values('date').filter(date__gte=oggi, erogation=False).order_by('date').count()

        print("e: " + str(e))
        print("noE: " + str(noE))

        context = {
            'erog': e,
            'noErog': noE,
            'righe': DatiRaccolti.objects.values().filter(date__gte=oggi)[:20],  # .order_by('-date') DA METTERE PER ORDINARE TABELLA
            'Righe': DatiRaccolti.objects.values().filter(date__gte=oggi)
        }

        return render(request, 'get_post.html', context)

    return HttpResponseForbidden


@csrf_exempt
def sendData(request):  # view che invia i dati per costruire il CHART erogazioni utente/automatiche lato html

    anno = request.GET.__getitem__('anno')
    mese = request.GET.__getitem__('mese')
    giorno = request.GET.__getitem__('giorno')


    stringa = anno + "-" + mese + "-" + giorno
    stringaI = giorno + "-" + mese + "-" + anno  # per categories grafico -- vedere come togliere lo zero davanti

    print(stringa)

    eA = DatiRaccolti.objects.values('date').filter(date__contains=stringa, erogation=True, userMod=False).order_by(
        'date').count()
    eU = DatiRaccolti.objects.values('date').filter(date__contains=stringa, erogation=True, userMod=True).order_by(
        'date').count()

    e = DatiRaccolti.objects.values('date').filter(date__contains=stringa, erogation=True).order_by(
        'date').count()  # erogazioni
    noE = DatiRaccolti.objects.values('date').filter(date__contains=stringa, erogation=False).order_by(
        'date').count()  # no erogazioni

    eG = DatiRaccolti.objects.values('date').filter(date__contains=stringa, erogation=True, timeMod=True).order_by(
        'date').count()  # giorno
    eN = DatiRaccolti.objects.values('date').filter(date__contains=stringa, erogation=True, timeMod=False).order_by(
        'date').count()  # notte

    print("eA: " + str(eA))
    print("eU: " + str(eU))

    print("e: " + str(e))
    print("noE: " + str(noE))

    print("eG: " + str(eG))
    print("eN: " + str(eN))

    context = {'righe': DatiRaccolti.objects.values().filter(date__contains=stringa).order_by('date'),
               # sistemare contains
               'giorno': stringaI, 'erogA': eA, 'erogU': eU, 'erog': e, 'noErog': noE, 'erogG': eG,
               'erogN': eN, 'Giorno': json.dumps(stringaI),
               'Righe': DatiRaccolti.objects.values().filter(date__contains=stringa)[:20]
               }

    return render(request, 'chartInside.html', context)


@csrf_exempt
def absentData(request):
    anno = request.GET.__getitem__('anno')
    mese = request.GET.__getitem__('mese')
    giorno = request.GET.__getitem__('giorno')

    if int(giorno) < 10:
        stringa = anno + "-" + mese + "-" + '0' + giorno  # + ' '
    else:
        stringa = anno + "-" + mese + "-" + giorno

    print(stringa)

    f = DatiRaccolti.objects.values().filter(date__contains=stringa)  # .order_by('date')  # sistemare contains
    lu = len(f)

    return JsonResponse(lu, safe=False)


@csrf_exempt
def ultimoDato(request):  # per aggiornamento tabella e chart

    stringa = datetime.today()
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

    oggi = datetime.today()
    # oggi = datetime.date(2019, 10, 22)

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

        # passato = datetime.date(annoP, meseP, giornoP)
        passato = datetime(annoP, meseP, giornoP).isoformat(' ')

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

        # passato = datetime.date(annoP, meseP, giornoP)
        passato = datetime(annoP, meseP, giornoP).isoformat(' ')

    print(passato)

    inizio = str(giornoP) + "-" + str(meseP) + "-" + str(annoP)
    fine = str(giornoC) + "-" + str(meseC) + "-" + str(annoC)

    eA = DatiRaccolti.objects.values('date').filter(date__gte=passato, date__lte=oggi, erogation=True,
                                                    userMod=False).order_by('date').count()
    eU = DatiRaccolti.objects.values('date').filter(date__gte=passato, date__lte=oggi, erogation=True,
                                                    userMod=True).order_by('date').count()

    e = DatiRaccolti.objects.values('date').filter(date__gte=passato, date__lte=oggi, erogation=True).order_by(
        'date').count()  # erogazioni
    noE = DatiRaccolti.objects.values('date').filter(date__gte=passato, date__lte=oggi, erogation=False).order_by(
        'date').count()  # no erogazioni

    eG = DatiRaccolti.objects.values('date').filter(date__gte=passato, date__lte=oggi, erogation=True,
                                                    timeMod=True).order_by('date').count()  # giorno
    eN = DatiRaccolti.objects.values('date').filter(date__gte=passato, date__lte=oggi, erogation=True,
                                                    timeMod=False).order_by('date').count()  # notte

    print("eA: " + str(eA))
    print("eU: " + str(eU))

    print("e: " + str(e))
    print("noE: " + str(noE))

    print("eG: " + str(eG))
    print("eN: " + str(eN))

    context = {'erogA': eA, 'erogU': eU, 'erog': e, 'noErog': noE, 'erogG': eG, 'erogN': eN,
               'inizio': inizio, 'fine': fine, 'Inizio': json.dumps(inizio), 'Fine': json.dumps(fine),
               'righe': DatiRaccolti.objects.values().filter(date__gte=passato, date__lte=oggi, erogation=True, userMod=False).order_by('date'),
               'Righe': DatiRaccolti.objects.values().filter(date__gte=passato, date__lte=oggi, erogation=True, userMod=False)[:20]
               }
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

    eG = DatiRaccolti.objects.values('date').filter(date__gte=stringa, erogation=True, timeMod=True).order_by(
        'date').count()  # giorno
    eN = DatiRaccolti.objects.values('date').filter(date__gte=stringa, erogation=True, timeMod=False).order_by(
        'date').count()  # notte

    # dovro' mettere tipo date__day = giorno, date__month = mese , ...

    print("eG: " + str(eG))
    print("eN: " + str(eN))

    erogazioni = [stringa, eG, eN]
    return JsonResponse(erogazioni, safe=False)

    # context = {'giorno': stringa, 'erogA': eA, 'erogU': eU}
    # return render(request, 'chartInside.html', context)

# view per creare l'array di date in un periodo (questi dati andranno a costituire l'asse x del grafico


def asseXIsto(request):
    # recupero il periodo -- dovro' recuperarlo dai parametri in request.GET

    inizio = datetime(2019, 11, 27).isoformat(' ')
    fine = datetime(2019, 12, 5).isoformat(' ')
    db = DatiRaccolti.objects.values('date').filter(date__range=(inizio, fine))

    # rendo db un array

    listDb = list()
    formatList = list()  # serve per renderizzare le date lato html

    for entry in db:
        listDb.append(entry['date'])

    # print("lista date: ", listDb)
    print(len(listDb))

    arrayDate = []
    arrayErog = []
    i = 0
    s = 0

    while i < len(listDb):
        x = listDb.pop(i)
        print("x: ", x)
        arrayDate.append(x)
        formatList.append(x.strftime("%d-%m-%y"))
        j = i + 1

        while (j < len(listDb)) and (listDb[j].year == x.year) and (listDb[j].month == x.month) and (listDb[j].day == x.day):
            j = j + 1
            s = j

        i = s

    print("arrayDate: ", arrayDate)

    # raccolgo i dati dell'asse y

    for k in range(len(arrayDate)):
        if k == len(arrayDate) - 1:  # cambiare eventualmente con contains
            e = DatiRaccolti.objects.values().filter(date__gte=arrayDate[k], date__lt=fine, erogation=True).count()

        else:
            e = DatiRaccolti.objects.values().filter(date__gte=arrayDate[k], date__lt=arrayDate[k+1], erogation=True).count()

        print("Le erogazioni del giorno " + str(arrayDate[k]) + " sono: " + str(e))
        arrayErog.append(e)

    print("arrayErog: ", arrayErog)

    context = {'arrayDate': json.dumps(formatList), 'arrayErog': arrayErog,
               'inizio': json.dumps(formatList[0]), 'fine': json.dumps(formatList[len(formatList) - 1])}

    return render(request, 'istog.html', context)



