# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from .models import DatiRaccolti
from django.views.decorators.csrf import csrf_exempt
import json


def index(request):
    return HttpResponse("<p> Food Dispenser Application </p>")


def profile(request):
    return HttpResponse("<p>Profile page of user </p>")


def home(request):  # renderizza i dati del database
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
        sensor_data.save()

        return HttpResponse()

    if request.method == 'GET':
        print('get')

    return HttpResponseForbidden


@csrf_exempt
def client(request):  # processa i dati inviati a seguito del click dell'utente

    if request.method == 'POST':
        print('post')
        print(request.body)
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)  # e' un oggetto python

        sensor_data = DatiRaccolti()
        sensor_data.userMod = body_data['userMod']

        sensor_data.save()

        return HttpResponse()

    if request.method == 'GET':
        print('get')
        return render(request, 'get_post.html')

    return HttpResponseForbidden
