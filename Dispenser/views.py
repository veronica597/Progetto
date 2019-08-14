# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import HttpResponse


def index(request):
    return HttpResponse("<p> Hello </p>")


def profile(request):
    return HttpResponse("<p>Profile page of user </p>")


