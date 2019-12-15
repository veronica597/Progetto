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


@csrf_exempt
def index(request):
    # return HttpResponse("<p> Food Dispenser Application </p>")
    return render(request, 'index.html')


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
        meseC = oggi.month
        giornoC = oggi.day
        annoC = oggi.year

        stringa = str(annoC) + "-" + str(meseC) + "-" + str(giornoC)
        print("stringa: ", stringa)

        e = DatiRaccolti.objects.values().filter(date__gte=stringa, erogation=True).order_by('date').count()
        noE = DatiRaccolti.objects.values().filter(date__gte=stringa, erogation=False).order_by('date').count()

        print("e: " + str(e))
        print("noE: " + str(noE))

        context = {
            'erog': e,
            'noErog': noE,
            'righe': DatiRaccolti.objects.values().filter(date__gte=stringa).order_by('-date')[:5],
            'Righe': DatiRaccolti.objects.values().filter(date__gte=stringa).order_by('-date')
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
        stringa = anno + "-" + mese + "-" + '0' + giorno
    else:
        stringa = anno + "-" + mese + "-" + giorno

    print(stringa)

    f = DatiRaccolti.objects.values().filter(date__contains=stringa)  # .order_by('date')
    lu = len(f)

    return JsonResponse(lu, safe=False)


@csrf_exempt
def absentDataPeriod(request):  # per periodo scelto da utente

    anno = request.GET.__getitem__('anno')
    mese = request.GET.__getitem__('mese')
    giorno = request.GET.__getitem__('giorno')

    stringaI = anno + "-" + mese + "-" + giorno

    annoF = int(request.GET.__getitem__('annoF'))
    meseF = int(request.GET.__getitem__('meseF'))
    giornoF = int(request.GET.__getitem__('giornoF'))

    # logica del 'giorno in più' per ovviare al problema della selezione del periodo

    mesi31 = [1, 3, 5, 7, 8, 10, 12]
    mesi30 = [4, 6, 9, 11]

    if meseF in mesi31:
        if giornoF == 31:
            giornoF = 1
            if meseF == 12:
                meseF = 1  # gennaio
            else:
                meseF = meseF + 1

        else:
            giornoF = giornoF + 1

    elif meseF in mesi30:
        if giornoF == 31:
            giornoF = 1
            meseF = meseF + 1

        else:
            giornoF = giornoF + 1

    elif meseF == 2:  # febbraio
        if giornoF == 28:
            giornoF = 1
            meseF = 3
        else:
            giornoF = giornoF + 1

    stringaF = str(annoF) + "-" + str(meseF) + "-" + str(giornoF)

    print(stringaI, stringaF)

    f = DatiRaccolti.objects.values().filter(date__gte=stringaI, date__lte=stringaF).order_by('date')
    lu = len(f)

    return JsonResponse(lu, safe=False)


@csrf_exempt
def ultimoDato(request):  # per aggiornamento tabella e chart

    oggi = datetime.today()

    meseC = oggi.month
    giornoC = oggi.day
    annoC = oggi.year

    stringa = str(annoC) + "-" + str(meseC) + "-" + str(giornoC)

    print("stringa: ", stringa)

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
def periodo(request):  # per filtraggio mese/settimana/periodo scelto dall'utente

    id = request.GET.__getitem__('id')
    print('id: ' + id)

    oggi = datetime.today()
    Oggi = datetime.today().isoformat(' ')

    meseC = oggi.month
    giornoC = oggi.day
    annoC = oggi.year

    fine = str(giornoC) + "-" + str(meseC) + "-" + str(annoC)  # intesa come stringa della data finale del periodo

    print("oggi: " + str(oggi))

    # in base al valore dell'id passato calcolo giorno mese scorso o giorno settimana scorsa o i giorni per il periodo scelto dall'utente

    if id == '1':  # mese
        print("mesee")
        giornoP = giornoC  # mantengo il giorno

        if meseC == 1:  # se e' gennaio cambio il mese ma anche l'anno
            meseP = 12
            annoP = annoC - 1

        else:
            meseP = meseC - 1
            annoP = annoC

        inizio = str(giornoP) + "-" + str(meseP) + "-" + str(annoP)  # intesa come stringa della data finale del periodo
        passato = datetime(annoP, meseP, giornoP).isoformat(' ')

    elif id == '0':  # settimana
        print("settimana")

        mesi31 = [1, 3, 5, 7, 8, 10, 12]
        mesi30 = [4, 6, 9, 11]

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

        inizio = str(giornoP) + "-" + str(meseP) + "-" + str(annoP)  # intesa come stringa della data finale del periodo
        passato = datetime(annoP, meseP, giornoP).isoformat(' ')

    elif id == '2':  # periodo scelto da utente
        print("periodo scelto dall'utente")

        meseP = int(request.GET.__getitem__('mese'))
        giornoP = int(request.GET.__getitem__('giorno'))
        annoP = int(request.GET.__getitem__('anno'))

        inizio = str(giornoP) + "-" + str(meseP) + "-" + str(annoP)  # intesa come stringa della data iniziale del periodo
        passato = datetime(annoP, meseP, giornoP).isoformat(' ')

        meseC = int(request.GET.__getitem__('meseF'))
        giornoC = int(request.GET.__getitem__('giornoF'))
        annoC = int(request.GET.__getitem__('annoF'))

        fine = str(giornoC) + "-" + str(meseC) + "-" + str(annoC)  # intesa come stringa della data finale del periodo

        # logica del 'giorno in più' per ovviare al problema della selezione del periodo

        mesi31 = [1, 3, 5, 7, 8, 10, 12]
        mesi30 = [4, 6, 9, 11]

        if meseC in mesi31:
            if giornoC == 31:
                giornoC = 1
                if meseC == 12:
                    meseC = 1  # gennaio
                else:
                    meseC = meseC + 1

            else:
                giornoC = giornoC + 1

        elif meseC in mesi30:
            if giornoC == 31:
                giornoC = 1
                meseC = meseC + 1

            else:
                giornoC = giornoC + 1

        elif meseC == 2:  # febbraio
            if giornoC == 28:
                giornoC = 1
                meseC = 3
            else:
                giornoC = giornoC + 1

        Oggi = datetime(annoC, meseC, giornoC).isoformat(' ')
        print("Oggi cambiato: ", Oggi)

    print("Il periodo selezionato e': ", passato, Oggi)

    # grafici

    eA = DatiRaccolti.objects.values('date').filter(date__gte=passato, date__lte=Oggi, erogation=True,
                                                    userMod=False).order_by('date').count()  # erogazioni modalita' automatica
    eU = DatiRaccolti.objects.values('date').filter(date__gte=passato, date__lte=Oggi, erogation=True,
                                                    userMod=True).order_by('date').count()  # erogazioni modalita' utente

    e = DatiRaccolti.objects.values('date').filter(date__gte=passato, date__lte=Oggi, erogation=True).order_by(
        'date').count()  # erogazioni
    noE = DatiRaccolti.objects.values('date').filter(date__gte=passato, date__lte=Oggi, erogation=False).order_by(
        'date').count()  # no erogazioni

    eG = DatiRaccolti.objects.values('date').filter(date__gte=passato, date__lte=Oggi, erogation=True,
                                                    timeMod=True).order_by('date').count()  # giorno
    eN = DatiRaccolti.objects.values('date').filter(date__gte=passato, date__lte=Oggi, erogation=True,
                                                    timeMod=False).order_by('date').count()  # notte

    print("eA: " + str(eA))
    print("eU: " + str(eU))

    print("e: " + str(e))
    print("noE: " + str(noE))

    print("eG: " + str(eG))
    print("eN: " + str(eN))

    # istogramma

    db = DatiRaccolti.objects.values('date').filter(date__gt=passato, date__lte=Oggi)

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
        formatList.append(x.strftime("%d-%m-%Y"))
        j = i + 1

        while (j < len(listDb)) and (listDb[j].year == x.year) and (listDb[j].month == x.month) and (listDb[j].day == x.day):
            j = j + 1
            s = j

        i = s

    # print("arrayDate: ", arrayDate)
    print("formatList: ", formatList)

    # raccolgo i dati dell'asse y

    for k in range(len(arrayDate)):
        if k == len(arrayDate) - 1:  # cambiare eventualmente con contains
            e = DatiRaccolti.objects.values().filter(date__gte=arrayDate[k], date__lt=Oggi, erogation=True).count()

        else:
            e = DatiRaccolti.objects.values().filter(date__gte=arrayDate[k], date__lt=arrayDate[k+1], erogation=True).count()

        print("Le erogazioni del giorno " + str(arrayDate[k]) + " sono: " + str(e))
        arrayErog.append(e)

    print("arrayErog: ", arrayErog)

    context = {'erogA': eA, 'erogU': eU, 'erog': e, 'noErog': noE, 'erogG': eG, 'erogN': eN,
               'righe': DatiRaccolti.objects.values().filter(date__gte=passato, date__lte=Oggi, erogation=True, userMod=False).order_by('date'),
               'Righe': DatiRaccolti.objects.values().filter(date__gte=passato, date__lte=Oggi, erogation=True, userMod=False)[:20],
               'arrayDate': json.dumps(formatList), 'arrayErog': arrayErog,
               'inizio': json.dumps(formatList[0]), 'fine': json.dumps(formatList[len(formatList) - 1]),  # per istogramma
               'Inizio': json.dumps(inizio), 'Fine': json.dumps(fine),  # per grafici
               }

    return render(request, 'statistics.html', context)





# Da eliminare dopo integrazione


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



