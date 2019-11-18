# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden, Http404
from .models import DatiRaccolti
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from django.core import serializers
from django.http import JsonResponse
from django.utils import timezone
from django.db import models
from django.db.models import Count, Q


def index(request):
    return HttpResponse("<p> Food Dispenser Application </p>")


def profile(request):
    return HttpResponse("<p>Profile page of user </p>")


@csrf_exempt
def home(request):  # renderizza i dati del database
    if request.method == 'GET':
        return render(request, 'index.html', {
            'righe': DatiRaccolti.objects.all(),
        })


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

    if request.method == 'POST':
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
        return render(request, 'get_post.html')

    return HttpResponseForbidden

#
# @csrf_exempt
# def ajax(request):
#     return render(request, 'ajax_test.html', )
#
#
# @csrf_exempt
# def visual(request):
#     increment = int(request.GET['append_increment'])
#     increment_to = increment + 10
#     return render(request, 'render_ajax.html', {
#         'righe': DatiRaccolti.objects.filter(timeMod=1)[increment:increment_to],
#     })


@csrf_exempt
def get_ajax(request):  # view che chiamo per avere l'ultimo dato postato per aggiornare la TABELLA

    def myConverter(o):
        if isinstance(o, datetime.datetime):
            return o.__str__()

    if request.is_ajax() or request.method == "GET":

        elementi = DatiRaccolti.objects.values().filter(date__gte="2019-11-05")
        # for el in elementi:
        #     elem.append(json.dumps(el, default=myConverter))
        #
        # print(elem)
        # dictionary = list(elementi)
        #print(dictionary)

        # id = len(elementi)
        # data = json.dumps(elementi)
        #data = serializers.serialize('json', elementi)
        #print(data)
        # element_id = json.dumps(id)
        # items = ["Mario", "Lorenzo", "Pino"]
        # data = json.dumps(dictionary, default=myConverter)

        # print(data)
        # print(elementi)
        # return HttpResponse(data, content_type="application/json")
        # x = DatiRaccolti.objects.values().filter(date__lte=timezone.datetime(2019, 10, 16, 13, 5, 27, 892171))

        lu = len(elementi)
        print(lu)
        f = elementi[0]  # lu - 1
        print(f)

        # print(data)
        return JsonResponse(f, safe=False)
        # return JsonResponse({'righe': list(elementi)})
        # return HttpResponse({'righe': elementi})
        # return render(request, "get_ajax.html", {'righe': elementi})
    else:
        raise Http404


@csrf_exempt
def viewData(request):  # view pagina utente -- dati giorno corrente -- TABELLA
    if request.method == 'GET':
        context = {'righe': DatiRaccolti.objects.values().filter(date__gte="2019-11-05")}  # dati del giorno corrente
        return render(request, "get_ajax.html", context)


@csrf_exempt
def LastDate(request):  # view che chiamo per avere i dati per aggiornare il CHART
    dataset = DatiRaccolti.objects \
        .values('date') \
        .filter(date__gte="2019-11-05") \
        .annotate(erogatedA=Count('date', filter=Q(erogation=True, userMod=False)),
                  erogatedU=Count('date', filter=Q(erogation=True, userMod=True))) \
        .order_by('date')

    categories = list()
    erogAutomatic = list()
    erogUser = list()

    for entry in dataset:
        categories.append('%s Class' % entry['date'])
        erogAutomatic.append(entry['erogatedA'])
        erogUser.append(entry['erogatedU'])

    # old_cat = categories
    # old_erogA = erogAutomatic
    # old_erogU = erogUser

    lastCat = categories[len(categories) - 1]  # l'ultima data
    print(lastCat)
    lastErogA = erogAutomatic[len(erogAutomatic) - 1]  # l'ultimo valore di erogazione automatica
    lastErogU = erogUser[len(erogUser) - 1]  # l'ultimo valore di erogazione utente

    # automatic_series = {
    #     'name': 'Erogazioni automatiche',
    #     'data': lastErogA,  # [old_erogA, lastErogA] vedere
    #     'color': 'green'
    # }
    #
    # user_series = {
    #     'name': 'Erogazioni utente',
    #     'data': lastErogU,  # [old_erogU, lastErogU] vedere
    #     'color': 'red'
    # }
    #
    # chart = {
    #     'chart': {'type': 'column'},
    #     'title': {'text': 'Romano Ts'},
    #     'xAxis': {'categories': lastCat},  # [old_cat, lastCat] vedere
    #     'series': [automatic_series, user_series]
    # }

    nicolino = json.dumps(lastCat)
    nicol = json.dumps(lastErogU)
    locin = json.dumps(lastErogA)

    macro = list()  # incapsulo gli ultimi dati in una lista
    macro.append(nicolino)
    macro.append(nicol)
    macro.append(locin)

    return JsonResponse(macro, safe=False)  # chart se passo tutto il chart modificato


@csrf_exempt
def chartData(request):  # view che renderizza il CHART "statico"
    dataset = DatiRaccolti.objects \
        .values('date') \
        .filter(date__gte="2019-11-05") \
        .annotate(erogatedA=Count('date', filter=Q(erogation=True, userMod=False)),
                  erogatedU=Count('date', filter=Q(erogation=True, userMod=True))) \
        .order_by('date')

    categories = list()
    erogAutomatic = list()
    erogUser = list()

    for entry in dataset:
        categories.append('%s Class' % entry['date'])
        erogAutomatic.append(entry['erogatedA'])
        erogUser.append(entry['erogatedU'])

    automatic_series = {
        'name': 'Erogazioni automatiche',
        'data': erogAutomatic,
        'color': 'green'
    }

    user_series = {
        'name': 'Erogazioni utente',
        'data': erogUser,
        'color': 'red'
    }

    chart = {
        'chart': {'type': 'column'},
        'title': {'text': 'Romano Ts'},
        'xAxis': {'categories': categories},
        'series': [automatic_series, user_series]
    }

    dump = json.dumps(chart)

    return render(request, 'chart.html', {'chart': dump})


@csrf_exempt
def grafico(request):
    context = {'righe': DatiRaccolti.objects.all().filter(date__gte="2019-11-05")}  # dati del giorno corrente
    return render(request, 'chartInside.html', context)


@csrf_exempt
def sendData(request):  # view che invia i dati per costruire il CHART lato html
    # print(request.body)
    # print(request.GET)
    anno = request.GET.__getitem__('anno')
    mese = request.GET.__getitem__('mese')
    giorno = request.GET.__getitem__('giorno')
    stringa = anno + "-" + mese + "-" + giorno
    # print(stringa)

    dataset = DatiRaccolti.objects \
        .values('date') \
        .filter(date__gte=stringa) \
        .annotate(erogatedA=Count('date', filter=Q(erogation=True, userMod=False)),
                  erogatedU=Count('date', filter=Q(erogation=True, userMod=True))) \
        .order_by('date')

    categories = list()
    erogAutomatic = list()
    erogUser = list()
    dateStringhe = list()

    for entry in dataset:
        categories.append('%s Class' % entry['date'])  #
        # print(entry['date'])
        # print(entry['date'].strftime("%d/%m/%y %H:%M:%S:%f"))
        dateStringhe.append(entry['date'].strftime("%d/%m/%y %H:%M:%S"))  # :%f per i millisecondi
        erogAutomatic.append(entry['erogatedA'])
        erogUser.append(entry['erogatedU'])

    # print(categories)
    # print(dateStringhe)
    cat = json.dumps(categories)
    # print(cat)
    autoE = json.dumps(erogAutomatic)
    userE = json.dumps(erogUser)

    macro = list()  # incapsulo gli ultimi dati in una lista
    macro.append(cat)
    macro.append(autoE)
    macro.append(userE)
    # print(macro)
    # print(json.dumps(macro))

    return JsonResponse(dateStringhe, safe=False)


@csrf_exempt
def ultimoDato(request):  # per aggiornamento tabella e chart
    # anno = request.GET.__getitem__('anno')
    # mese = request.GET.__getitem__('mese')
    # giorno = request.GET.__getitem__('giorno')
    # stringa = anno + "-" + mese + "-" + giorno
    elementi = DatiRaccolti.objects.values().filter(date__gte='2019-11-05')  # stringa

    # .strftime("%b. %d, %Y, %H:%M %p"))  # :%f per i millisecondi

    lu = len(elementi)
    # print(lu)
    # f = elementi[lu] # invio sempre l'ultimo elemento
    f = elementi[0]

    print(f)

    return JsonResponse(f, safe=False)



