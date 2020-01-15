# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, Http404
from .models import DatiRaccolti
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from django.http import JsonResponse


@csrf_exempt
def index(request):
    return render(request, 'index.html')


@csrf_exempt
def sensor(request):  # processa i dati da inserire nel database -- e' la view a cui fa la post l'esp8266

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
def client(request):  # processa i dati del giorno corrente

    if request.method == 'GET':
        print('get')
        today = datetime.today()
        monthC = today.month
        dayC = today.day
        yearC = today.year

        stringa = str(yearC) + "-" + str(monthC) + "-" + str(dayC)
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

        return render(request, 'getPost.html', context)

    return HttpResponseForbidden


@csrf_exempt
def sendData(request):  # view che invia i dati per costruire i CHART lato html per i singoli giorni

    year = request.GET.__getitem__('anno')
    month = request.GET.__getitem__('mese')
    day = request.GET.__getitem__('giorno')

    if int(day) < 10:
        stringa = year + "-" + month + "-" + "0" + day  # l'aggiunta dello 0 e' per contains
        stringaI = "0" + day + "-" + month + "-" + year  # per il titolo della pagina html
    else:
        stringa = year + "-" + month + "-" + day
        stringaI = day + "-" + month + "-" + year  # per il titolo della pagina html

    print("STRINGA filtraggio: ", stringa)

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
               'erogA': eA, 'erogU': eU, 'erog': e, 'noErog': noE, 'erogG': eG, 'erogN': eN,
               'giorno': stringaI, 'Giorno': json.dumps(stringaI),  # stringaI
               'Righe': DatiRaccolti.objects.values().filter(date__contains=stringa)[:20]
               }

    return render(request, 'chartInside.html', context)


@csrf_exempt
def absentData(request):  # per controllare la presenza di dati per un giorno singolo selezionato dall'utente
    year = request.GET.__getitem__('anno')
    month = request.GET.__getitem__('mese')
    day = request.GET.__getitem__('giorno')

    if int(day) < 10:   # pensare di mettere lo 0 per il mese
        stringa = year + "-" + month + "-" + '0' + day  # lo 0 e' per contains
    else:
        stringa = year + "-" + month + "-" + day

    print(stringa)

    f = DatiRaccolti.objects.values().filter(date__contains=stringa)
    lu = len(f)

    return JsonResponse(lu, safe=False)


@csrf_exempt
def absentDataPeriod(request):  # per Period scelto da utente

    print("view absentDataPeriod")

    year = request.GET.__getitem__('anno')
    month = request.GET.__getitem__('mese')
    day = request.GET.__getitem__('giorno')

    # in questo caso non mi serve aggiungere lo 0 perche' non utilizzo contains

    stringI = year + "-" + month + "-" + day

    yearF = int(request.GET.__getitem__('annoF'))
    monthF = int(request.GET.__getitem__('meseF'))
    dayF = int(request.GET.__getitem__('giornoF'))

    # logica del 'giorno in più' per ovviare al problema della selezione del Period

    months31 = [1, 3, 5, 7, 8, 10, 12]
    months30 = [4, 6, 9, 11]

    if monthF in months31:
        if dayF == 31:
            dayF = 1
            if monthF == 12:
                monthF = 1  # gennaio
                yearF = yearF + 1
            else:
                monthF = monthF + 1

        else:
            dayF = dayF + 1

    elif monthF in months30:
        if dayF == 30:
            dayF = 1
            monthF = monthF + 1

        else:
            dayF = dayF + 1

    elif monthF == 2:  # febbraio
        if dayF == 28:
            dayF = 1
            monthF = 3
        else:
            dayF = dayF + 1

    stringF = str(yearF) + "-" + str(monthF) + "-" + str(dayF)

    print(stringI, stringF)

    f = DatiRaccolti.objects.values().filter(date__gte=stringI, date__lte=stringF).order_by('date')
    lu = len(f)

    return JsonResponse(lu, safe=False)


@csrf_exempt
def absentDataWM(request):  # per verificare la presenza di dati nell'ultima settimana e nell'ultimo mese
    print("view absentDataWM")
    id = request.GET.__getitem__('id')
    print('id: ' + id)

    today = datetime.today()

    monthC = today.month
    dayC = today.day
    yearC = today.year

    end = str(yearC) + "-" + str(monthC) + "-" + str(dayC)

    print("oggi: " + str(today))

    # in base al valore dell'id passato calcolo giorno mese scorso o giorno settimana scorsa

    if id == '1':  # mese
        print("mesee")
        dayP = dayC  # mantengo il giorno

        if monthC == 1:  # se e' gennaio cambio il mese ma anche l'anno
            monthP = 12
            yearP = yearC - 1

        else:
            monthP = monthC - 1
            yearP = yearC

        past = str(yearP) + "-" + str(monthP) + "-" + str(dayP)

    elif id == '0':  # settimana
        print("settimana")

        months31 = [1, 3, 5, 7, 8, 10, 12]
        months30 = [4, 6, 9, 11]

        if dayC <= 7:
            yearP = yearC
            monthP = monthC - 1

            if monthC == 1:
                monthP=12
                yearP = yearC - 1

            if monthP in months31:
                dayP = 31 + (dayC - 7)

            elif monthP in months30:
                dayP = 30 + (dayC - 7)

            elif monthP == 2:
                dayP = 28 + (dayC - 7)

            print("meseP : ", monthP)

        else:
            monthP = monthC  # mantengo il mese
            dayP = dayC - 7
            yearP = yearC

        past = str(yearP) + "-" + str(monthP) + "-" + str(dayP)

    print("Il Periodo selezionato e': ", past, end)

    f = DatiRaccolti.objects.values().filter(date__gte=past, date__lte=end).order_by('date')
    lu = len(f)
    print("lunghezza: ", lu)

    dataToSend = [lu, past, end]  # Oggi

    return JsonResponse(dataToSend, safe=False)


@csrf_exempt
def LastAdded(request):  # per aggiornamento tabella e chart

    today = datetime.today()

    monthC = today.month
    dayC = today.day
    yearC = today.year

    string = str(yearC) + "-" + str(monthC) + "-" + str(dayC)

    print("stringa: ", string)

    elementi = DatiRaccolti.objects.values().filter(date__gte=string)

    lu = len(elementi)
    print(lu)
    if lu == 0:  # il database non contiene dati per il giorno corrente
        f = "Non ci sono erogazioni per il giorno corrente"

    else:
        f = elementi[lu - 1]  # invio sempre l'ultimo elemento

    print(f)

    return JsonResponse(f, safe=False)


@csrf_exempt
def Period(request):  # per filtraggio mese/settimana/Period scelto dall'utente -- versione che si combina con absentDataWM

    print("view Period")

    id = request.GET.__getitem__('id')
    print('id: ' + id)

    if id == '0' or id == '1':
        noData = request.GET.__getitem__('noData')
        print('noData: ' + noData)

        if id == '0' and noData == '1':  # se ho richiesto i dati dell'ultima settimana e NON ci sono
            print("non ci sono dati per l'ultima settimana !!")

            # se voglio che nel titolo ci siano le date devo fare così
            monthC = int(request.GET.__getitem__('meseF'))
            dayC = int(request.GET.__getitem__('giornoF'))
            yearC = int(request.GET.__getitem__('annoF'))

            today = str(yearC) + "-" + str(monthC) + "-" + str(dayC)

            if dayC < 10:
                if monthC < 10:
                    end = "0" + str(dayC) + "-0" + str(monthC) + "-" + str(yearC)
                else:
                    end = "0" + str(dayC) + "-" + str(monthC) + "-" + str(yearC)
            else:
                if monthC < 10:
                    end = str(dayC) + "-0" + str(monthC) + "-" + str(yearC)
                else:
                    end = str(dayC) + "-" + str(monthC) + "-" + str(yearC)

            monthP = int(request.GET.__getitem__('mese'))
            dayP = int(request.GET.__getitem__('giorno'))
            yearP = int(request.GET.__getitem__('anno'))

            past = str(yearP) + "-" + str(monthP) + "-" + str(dayP)

            if dayP < 10:
                if monthP < 10:
                    beginning = "0" + str(dayP) + "-0" + str(monthP) + "-" + str(yearP)
                else:
                    beginning = "0" + str(dayP) + "-" + str(monthP) + "-" + str(yearP)
            else:
                if monthP < 10:
                    beginning = str(dayP) + "-0" + str(monthP) + "-" + str(yearP)
                else:
                    beginning = str(dayP) + "-" + str(monthP) + "-" + str(yearP)

            print("Il Period selezionato e': ", past, today)

            mess = "There are no data for last week"

            context = {"mess": mess,
                       'Inizio1': beginning, 'Fine1': end  # per mettere nel titolo della pagina
                       }
            return render(request, 'statistics.html', context)

        elif id == '1' and noData == '1':  # se ho richiesto i dati dell'ultimo mese e NON ci sono
            print("non ci sono dati per l'ultimo mese !!")

            # se voglio che nel titolo ci siano le date devo fare così
            monthC = int(request.GET.__getitem__('meseF'))
            dayC = int(request.GET.__getitem__('giornoF'))
            yearC = int(request.GET.__getitem__('annoF'))

            today = str(yearC) + "-" + str(monthC) + "-" + str(dayC)

            if dayC < 10:
                if monthC < 10:
                    end = "0" + str(dayC) + "-0" + str(monthC) + "-" + str(yearC)
                else:
                    end = "0" + str(dayC) + "-" + str(monthC) + "-" + str(yearC)
            else:
                if monthC < 10:
                    end = str(dayC) + "-0" + str(monthC) + "-" + str(yearC)
                else:
                    end = str(dayC) + "-" + str(monthC) + "-" + str(yearC)

            monthP = int(request.GET.__getitem__('mese'))
            dayP = int(request.GET.__getitem__('giorno'))
            yearP = int(request.GET.__getitem__('anno'))

            past = str(yearP) + "-" + str(monthP) + "-" + str(dayP)

            if dayP < 10:
                if monthP < 10:
                    beginning = "0" + str(dayP) + "-0" + str(monthP) + "-" + str(yearP)
                else:
                    beginning = "0" + str(dayP) + "-" + str(monthP) + "-" + str(yearP)
            else:
                if monthP < 10:
                    beginning = str(dayP) + "-0" + str(monthP) + "-" + str(yearP)
                else:
                    beginning = str(dayP) + "-" + str(monthP) + "-" + str(yearP)

            print("Il Period selezionato e': ", past, today)

            mess = "There are no data for last month"
            context = {"mess": mess,
                       'Inizio1': beginning, 'Fine1': end  # per mettere nel titolo della pagina
                       }
            return render(request, 'statistics.html', context)

        elif noData == '0':

            print("settimana o mese")

            monthC = int(request.GET.__getitem__('meseF'))
            dayC = int(request.GET.__getitem__('giornoF'))
            yearC = int(request.GET.__getitem__('annoF'))

            today = str(yearC) + "-" + str(monthC) + "-" + str(dayC)

            if dayC < 10:
                if monthC < 10:
                    end = "0" + str(dayC) + "-0" + str(monthC) + "-" + str(yearC)
                else:
                    end = "0" + str(dayC) + "-" + str(monthC) + "-" + str(yearC)
            else:
                if monthC < 10:
                    end = str(dayC) + "-0" + str(monthC) + "-" + str(yearC)
                else:
                    end = str(dayC) + "-" + str(monthC) + "-" + str(yearC)

            # end = str(annoC) + "-" + str(meseC) + "-" + str(giornoC)  # per ultima data istogramma

            monthP = int(request.GET.__getitem__('mese'))
            dayP = int(request.GET.__getitem__('giorno'))
            yearP = int(request.GET.__getitem__('anno'))

            past = str(yearP) + "-" + str(monthP) + "-" + str(dayP)

            if dayP < 10:
                if monthP < 10:
                    beginning = "0" + str(dayP) + "-0" + str(monthP) + "-" + str(yearP)
                else:
                    beginning = "0" + str(dayP) + "-" + str(monthP) + "-" + str(yearP)
            else:
                if monthP < 10:
                    beginning = str(dayP) + "-0" + str(monthP) + "-" + str(yearP)
                else:
                    beginning = str(dayP) + "-" + str(monthP) + "-" + str(yearP)

            print("Il Period selezionato e': ", past, today)

            # grafici

            eA = DatiRaccolti.objects.values('date').filter(date__gte=past, date__lte=today, erogation=True,
                                                            userMod=False).order_by('date').count()  # erogazioni modalita' automatica
            eU = DatiRaccolti.objects.values('date').filter(date__gte=past, date__lte=today, erogation=True,
                                                            userMod=True).order_by('date').count()  # erogazioni modalita' utente

            e = DatiRaccolti.objects.values('date').filter(date__gte=past, date__lte=today, erogation=True).order_by(
                'date').count()  # erogazioni
            noE = DatiRaccolti.objects.values('date').filter(date__gte=past, date__lte=today, erogation=False).order_by(
                'date').count()  # no erogazioni

            eG = DatiRaccolti.objects.values('date').filter(date__gte=past, date__lte=today, erogation=True,
                                                            timeMod=True).order_by('date').count()  # giorno
            eN = DatiRaccolti.objects.values('date').filter(date__gte=past, date__lte=today, erogation=True,
                                                            timeMod=False).order_by('date').count()  # notte

            print("eA: " + str(eA))
            print("eU: " + str(eU))

            print("e: " + str(e))
            print("noE: " + str(noE))

            print("eG: " + str(eG))
            print("eN: " + str(eN))

            # istogramma

            db = DatiRaccolti.objects.values('date').filter(date__gt=past, date__lte=today)

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
                x = listDb[i]
                print("i: ", i)
                print("x: ", x)
                print("")
                arrayDate.append(x)
                formatList.append(x.strftime("%d-%m-%Y"))  # giorni e mesi < 10 hanno lo zero davanti
                j = i + 1

                while (j < len(listDb)) and (listDb[j].year == x.year) and (listDb[j].month == x.month) and (listDb[j].day == x.day):
                    j = j + 1
                    s = j
                    print("s: ", s)

                i = s

            # print("arrayDate: ", arrayDate)
            print("formatList: ", formatList)

            # raccolgo i dati dell'asse y

            for k in range(len(arrayDate)):
                if k == len(arrayDate) - 1:  # cambiare eventualmente con contains
                    e = DatiRaccolti.objects.values().filter(date__gte=arrayDate[k], date__lt=today, erogation=True).count()

                else:
                    e = DatiRaccolti.objects.values().filter(date__gte=arrayDate[k], date__lt=arrayDate[k+1], erogation=True).count()

                print("Le erogazioni del giorno " + str(arrayDate[k]) + " sono: " + str(e))
                arrayErog.append(e)

            print("arrayErog: ", arrayErog)

            context = {'erogA': eA, 'erogU': eU, 'erog': e, 'noErog': noE, 'erogG': eG, 'erogN': eN,
                       'righe': DatiRaccolti.objects.values().filter(date__gte=past, date__lte=today).order_by('date'),
                       'Righe': DatiRaccolti.objects.values().filter(date__gte=past, date__lte=today)[:20],
                       'arrayDate': json.dumps(formatList), 'arrayErog': arrayErog,
                       'Inizio': json.dumps(beginning), 'Fine': json.dumps(end),  # per grafici
                       'Inizio1': beginning, 'Fine1': end,  # per titolo pagina
                       'start': json.dumps(past), 'end': json.dumps(today),
                       }

            return render(request, 'statistics.html', context)

    else:  # id == 2

        print("Period scelto dall'utente")
        monthP = int(request.GET.__getitem__('mese'))
        dayP = int(request.GET.__getitem__('giorno'))
        yearP = int(request.GET.__getitem__('anno'))

        past = str(yearP) + "-" + str(monthP) + "-" + str(dayP)

        if dayP < 10:
            if monthP < 10:
                beginning = "0" + str(dayP) + "-0" + str(monthP) + "-" + str(yearP)
            else:
                beginning = "0" + str(dayP) + "-" + str(monthP) + "-" + str(yearP)
        else:
            if monthP < 10:
                beginning = str(dayP) + "-0" + str(monthP) + "-" + str(yearP)
            else:
                beginning = str(dayP) + "-" + str(monthP) + "-" + str(yearP)

        monthC = int(request.GET.__getitem__('meseF'))
        dayC = int(request.GET.__getitem__('giornoF'))
        yearC = int(request.GET.__getitem__('annoF'))

        if dayC < 10:
            if monthC < 10:
                end = "0" + str(dayC) + "-0" + str(monthC) + "-" + str(yearC)
            else:
                end = "0" + str(dayC) + "-" + str(monthC) + "-" + str(yearC)
        else:
            if monthC < 10:
                end = str(dayC) + "-0" + str(monthC) + "-" + str(yearC)
            else:
                end = str(dayC) + "-" + str(monthC) + "-" + str(yearC)

        end = str(yearC) + "-" + str(monthC) + "-" + str(dayC)  # per ultima data istogramma

        # logica del 'giorno in più' per ovviare al problema della selezione del Period

        months31 = [1, 3, 5, 7, 8, 10, 12]
        months30 = [4, 6, 9, 11]

        if monthC in months31:
            if dayC == 31:
                dayC = 1
                if monthC == 12:
                    monthC = 1  # gennaio
                    yearC = yearC + 1  # aggiorno l'anno
                else:
                    monthC = monthC + 1

            else:
                dayC = dayC + 1

        elif monthC in months30:
            if dayC == 30:
                dayC = 1
                monthC = monthC + 1

            else:
                dayC = dayC + 1

        elif monthC == 2:  # febbraio
            if dayC == 28:
                dayC = 1
                monthC = 3
            else:
                dayC = dayC + 1

        today = str(yearC) + "-" + str(monthC) + "-" + str(dayC)
        print("Oggi cambiato: ", today)

        print("Il Period selezionato e': ", past, today)

        # grafici

        eA = DatiRaccolti.objects.values('date').filter(date__gte=past, date__lte=today, erogation=True,
                                                        userMod=False).order_by('date').count()  # erogazioni modalita' automatica
        eU = DatiRaccolti.objects.values('date').filter(date__gte=past, date__lte=today, erogation=True,
                                                        userMod=True).order_by('date').count()  # erogazioni modalita' utente

        e = DatiRaccolti.objects.values('date').filter(date__gte=past, date__lte=today, erogation=True).order_by(
            'date').count()  # erogazioni
        noE = DatiRaccolti.objects.values('date').filter(date__gte=past, date__lte=today, erogation=False).order_by(
            'date').count()  # no erogazioni

        eG = DatiRaccolti.objects.values('date').filter(date__gte=past, date__lte=today, erogation=True,
                                                        timeMod=True).order_by('date').count()  # giorno
        eN = DatiRaccolti.objects.values('date').filter(date__gte=past, date__lte=today, erogation=True,
                                                        timeMod=False).order_by('date').count()  # notte

        print("eA: " + str(eA))
        print("eU: " + str(eU))

        print("e: " + str(e))
        print("noE: " + str(noE))

        print("eG: " + str(eG))
        print("eN: " + str(eN))

        # istogramma

        db = DatiRaccolti.objects.values('date').filter(date__gt=past, date__lte=today)

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
            x = listDb[i]
            print("i: ", i)
            print("x: ", x)
            print("")
            arrayDate.append(x)
            formatList.append(x.strftime("%d-%m-%Y"))
            j = i + 1

            while (j < len(listDb)) and (listDb[j].year == x.year) and (listDb[j].month == x.month) and (listDb[j].day == x.day):
                j = j + 1
                s = j
                print("s: ", s)

            i = s

        print("formatList: ", formatList)

        # raccolgo i dati dell'asse y

        for k in range(len(arrayDate)):
            if k == len(arrayDate) - 1:  # cambiare eventualmente con contains
                e = DatiRaccolti.objects.values().filter(date__gte=arrayDate[k], date__lt=today, erogation=True).count()

            else:
                e = DatiRaccolti.objects.values().filter(date__gte=arrayDate[k], date__lt=arrayDate[k+1], erogation=True).count()

            print("Le erogazioni del giorno " + str(arrayDate[k]) + " sono: " + str(e))
            arrayErog.append(e)

        print("arrayErog: ", arrayErog)

        context = {'erogA': eA, 'erogU': eU, 'erog': e, 'noErog': noE, 'erogG': eG, 'erogN': eN,
                   'righe': DatiRaccolti.objects.values().filter(date__gte=past, date__lte=today).order_by('date'),
                   'Righe': DatiRaccolti.objects.values().filter(date__gte=past, date__lte=today)[:20],
                   'arrayDate': json.dumps(formatList), 'arrayErog': arrayErog,
                   'Inizio': json.dumps(beginning), 'Fine': json.dumps(end),  # per grafici
                   'Inizio1': beginning, 'Fine1': end,
                   'start': json.dumps(past), 'end': json.dumps(end),  # per asse x istogramma con tutti giorni
                   }

        return render(request, 'statistics.html', context)





