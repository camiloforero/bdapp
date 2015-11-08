from django.db.models import Sum
from django.shortcuts import render

from bam.models import LC, Semana, Puntajes

import itertools

def ranking(request, area, semana):
    kwargs = {"%s__gt"%area:0}
    puntajes = Puntajes.objects.filter(semana=semana, **kwargs).order_by("-%s" % area)
    context = {'puntajes':puntajes, 'area':area, 'semana':semana}
    return render(request, 'bam/ranking.html', context)

def millas_lc(request, nombre_lc, semana):
    nombre_lc = "AIESEC %s" % nombre_lc.replace("_", " ")
    areas = ['IGCDP', 'OGCDP', 'IGIP', 'OGIP']
    tipos_puntaje = ['ip', 'ma', 'bonus']
    product = map(''.join, list(itertools.product(tipos_puntaje, ["_"], areas)) + areas)
    kwargs = {key: Sum(key) for key in product}
    puntajes = Puntajes.objects.filter(lc__nombre=nombre_lc, semana__lte=semana).aggregate(**kwargs)
    context = {'product': product,'puntajes':puntajes, 'areas':areas, 'tipos': tipos_puntaje}
    return render(request, 'bam/lc.html', context)
# Create your views here.
