# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, FileResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.template.loader import render_to_string

from aux import generatePdf, QDICT
from forms import InscriptionForm, UserForm, ConfirmationForm, AcceptanceForm, CartasForm
from io import BytesIO
from reportlab.lib import styles
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from models import Trainee
from webodt.converters import converter

import csv
import os
import random
import string

# Create your views here.
@login_required
def index(request):
    """Muestra la página principal que ven los empresarios cuando entran a la aplicación"""
    if request.user.is_superuser:
        return redirect('admin:index')
    if(request.user.empresario):
        return render (request, 'fileManager/index.html')

@login_required
def seleccion(request):
    """Esta vista permite que el administrador de la empresa vea a todos los trainees que hacen parte de dicha empresa y sobre los cuales aún no han tomado una decisión. Le da la opción de aceptar o rechazar a cada uno de estos aplicantes."""
    trainees = request.user.empresario.empresa.trainees.filter(*QDICT["por_aceptar"]).select_related("user").order_by('grupo')
    context = {'trainees':trainees}
    return render (request, 'fileManager/seleccion.html', context)


def confirmation(request):
    if request.method == 'POST':
        trainee = Trainee.objects.get(code=request.POST["code2"])
        form = ConfirmationForm(request.POST, request.FILES, instance=trainee)
        if form.is_valid():
            form.save()
            trainee.confirmado = True
            trainee.save()
            return HttpResponse("success")
        else:
            context = {
                'forms':[form,], 
                'form_message':"Congratulations for being accepted! Please fill out this additional information so we can get started processing your immigration papers",
                'locale':'en-US',
            }
            return render(request, 'fileManager/form.html', context)

    else:
        form = ConfirmationForm()
        context = {
            'forms':[form,], 
            'form_message':"Congratulations for being accepted! Please fill out this additional information so we can get started processing your immigration papers",
                'locale':'en-US',
            }
        return render(request, 'fileManager/form.html', context)

@login_required
def seleccionar(request, trainee, aprobado):
    if request.method == 'POST':
        oTrainee = Trainee.objects.get(pk=trainee)
        form = AcceptanceForm(request.POST, instance=oTrainee)
        if form.is_valid():
            form.save()
            datos = {
                "code": oTrainee.code,
                "tn_id": oTrainee.empresa.tn_id,
                "full_name": str(oTrainee),
                "start_date": oTrainee.fecha_inicio_practica.strftime("%d of %B"),
		"root_url": settings.BDAPP_ROOT_URL,
            }
            mensaje = render_to_string('fileManager/emails/accepted.txt', datos)
            send_mail('You have been accepted', mensaje, 'maria.cubillos@aiesec.net', [oTrainee.user.email], fail_silently=False)
            oTrainee.estado=True
            oTrainee.save()
            return HttpResponseRedirect(reverse("fileManager:seleccion"))
        else:
            context = {
                'forms':[form,],
                'form_message':u"Por favor ingrese las fechas de inicio y de fin de la práctica del seleccionado",
                'url':reverse('fileManager:seleccionar', kwargs={'trainee':trainee, 'aprobado':'si'}),
                'locale':'es-CO',
            }
            return render(request, 'fileManager/form.html', context)


    else:
        estados = {"si":True, "no":False}
        oTrainee = Trainee.objects.get(pk=trainee)
        estado = estados[aprobado]
        if(estado):
            form = AcceptanceForm(instance=oTrainee)
            context = {
                'forms':[form,],
                'form_message':u"Por favor ingrese las fechas de inicio y de fin de la práctica del seleccionado",
                'url':reverse('fileManager:seleccionar', kwargs={'trainee':trainee, 'aprobado':'si'}),
                'locale':'es-CO',
            }
            return render(request, 'fileManager/form.html', context)

        else:
            oTrainee.estado = estado
            mensaje = render_to_string('fileManager/emails/rejected.txt', {})
            send_mail('You have been rejected', mensaje, 'maria.cubillos@aiesec.net', [oTrainee.user.email], fail_silently=False)
            oTrainee.save()
            return HttpResponseRedirect(reverse("fileManager:seleccion"))

@login_required
def ver_aceptados(request):
    trainees = request.user.empresario.empresa.trainees.filter(*QDICT['aceptados']).select_related("user")
    context = {'trainees':trainees}
    return render (request, 'fileManager/aceptados.html', context)

@login_required
def ver_cartas(request):
    trainees = request.user.empresario.empresa.trainees.filter(*QDICT['cartas_generadas'])
    context = {'trainees':trainees}
    return render (request, 'fileManager/ver_cartas.html', context)

@login_required
def subir_cartas(request, trainee):
    if request.method == 'POST':
        oTrainee = Trainee.objects.get(pk=trainee)
        form = CartasForm(request.POST, request.FILES, instance=oTrainee)
        if form.is_valid():
	    import os
	    lang = os.environ['LANG']
            form.save()
            return HttpResponseRedirect(reverse("fileManager:ver_cartas"))
        else:
            context = {
                'forms':[form,],
                'form_message':u"Por favor suba las dos cartas de aceptación del practicante, firmadas",
                'url':reverse('fileManager:subir_cartas', kwargs={'trainee':trainee}),
                'locale':'es-CO',
            }
            return render(request, 'fileManager/form.html', context)


    else:
        form = CartasForm()
        context = {
            'forms':[form,],
            'form_message':u"Por favor suba las dos cartas de aceptación del practicante, firmadas",
            'url':reverse('fileManager:subir_cartas', kwargs={'trainee':trainee}),
            'locale':'es-CO',
        }
        return render(request, 'fileManager/form.html', context)

@login_required
def ver_legalizados(request):
    trainees = request.user.empresario.empresa.trainees.filter(*QDICT['cartas_firmadas'])
    context = {'trainees':trainees}
    return render (request, 'fileManager/ver_legalizados.html', context)


@login_required
def createTemplate(request):
    send_mail('Subject here', 'Here is the message.', 'postmaster@co.aiesec.org', ['camilo.forero@aiesec.net'], fail_silently=False)
    context = {'full_name': 'Enakshi Manohar'}
    pdf = generatePdf('memodeal.odt', context)
    response = FileResponse(pdf, 'rb')
    return response

@login_required
def media_xsendfile(request, path, document_root):
    response = HttpResponse()
    response['Content-Type'] = ''
    response['X-Sendfile'] = (os.path.join(document_root, path)).encode('utf-8')
    return response



def crearEscarapelas(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="booklets_trainees.pdf"'
    datos = open('/home/camilo/public/trainees.csv', 'r')
    reader = csv.DictReader(datos)
    actual = 0
    ultimoError = 38 
    for row in reader:
        if actual < ultimoError:
            actual += 1
            continue
        actual += 1
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=(1700,2200))
        ttfFile = os.path.join('/home/camilo/public/canarottf', 'Canaro-Medium.ttf')
        pdfmetrics.registerFont(TTFont("Canaro", ttfFile))
        urlBase = '/home/camilo/public/BOOKLET/p-%i.png'
        p.drawImage(urlBase%1, 0, 0)
        p.showPage()
        p.drawImage(urlBase%2,0,0)
        p.showPage()
        p.drawImage(urlBase%3,0,0)
        p.setFont('Canaro', 50)
        p.drawString(423, 1782, row["Trainee stand 1"].decode("cp1252"))
        p.drawString(423, 1708, row["Trainee stand 2"].decode("cp1252"))

        p.showPage()
        p.drawImage(urlBase%4,0,0)
        p.showPage()
        p.drawImage(urlBase%5,0,0)
        p.showPage()
        p.drawImage(urlBase%6,0,0)
        p.showPage()
        p.drawImage(urlBase%7,0,0)
        p.showPage()
        p.drawImage(urlBase%8,0,0)
        p.setFont('Canaro', 40)
        p.drawString(550, 1539, row["Region"].decode("cp1252"))
        p.drawString(607, 1403, row["Country"].decode("cp1252"))
        p.drawCentredString(1400, 1259, row["Stand #"])
        p.drawString(826, 1141, row["AIESEC Coordinatior"])
        p.showPage()
        p.drawImage(urlBase%9,0,0)
        p.showPage()
        p.drawImage(urlBase%10,0,0)
        p.setFont('Canaro', 60)
        p.drawString(584, 1776, row["PopulationV"].decode("cp1252"))
        p.drawString(431, 1649, row["Capital"].decode("cp1252"))
        p.drawString(858, 1524, row["Capital's Population  "])
        p.setFont('Canaro', 30)
        try:
            p.drawString(533, 627, row["Flags Link "].split("//")[1])
        except(IndexError):
            pass
        try:
            p.drawString(672, 495, row["Currenci Link"].decode("cp1252").split("//")[1])
        except(IndexError):
            pass
        p.showPage()
        p.drawImage(urlBase%11,0,0)
        p.setFont('Canaro', 60)
        languages = row["Languages spoken"].decode("cp1252").split(", ")
        try:
            if languages[0]:
                p.drawString(861, 1731, languages[0])
            if languages[1]:
                p.drawString(861, 1651, languages[1])
            if languages[2]:
                p.drawString(861, 1571, languages[2])
        except(IndexError):
            pass
        p.showPage()
        p.drawImage(urlBase%12,0,0)
        p.showPage()
        p.drawImage(urlBase%13,0,0)
        p.showPage()
        p.drawImage(urlBase%14,0,0)
        p.save()
        pdf = buffer.getvalue()
        buffer.close()
        f = open('/home/camilo/public/bookletsFinales/%s.pdf'%row["Country"].replace('/', '-'), 'wb')
        f.write(pdf)
        f.close()
        
    return response


def crearBookletsAfuera2(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="booklets_trainees.pdf"'
    datos = open('/home/camilo/public/fuera.csv', 'r')
    reader = csv.DictReader(datos)
    actual = 0
    ultimoError = 26 
    for row in reader:
        if actual < ultimoError:
            actual += 1
            continue
        actual += 1
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=(1700,2200))
        ttfFile = os.path.join('/home/camilo/public/canarottf', 'Canaro-Medium.ttf')
        pdfmetrics.registerFont(TTFont("Canaro", ttfFile))
        urlBase = '/home/camilo/public/fuera/fuera-%i.png'
        p.drawImage(urlBase%1, 0, 0)
        p.showPage()
        p.drawImage(urlBase%2,0,0)
        p.showPage()
        p.drawImage(urlBase%3,0,0)
        p.setFont('Canaro', 50)
        p.drawString(326, 1712, row["TRAINEE"].decode("cp1252"))

        p.showPage()
        p.drawImage(urlBase%4,0,0)
        p.showPage()
        p.drawImage(urlBase%5,0,0)
        p.showPage()
        p.drawImage(urlBase%6,0,0)
        p.showPage()
        p.drawImage(urlBase%7,0,0)
        p.setFont('Canaro', 40)
        p.drawString(570, 1475, row["REGION"].decode("cp1252"))
        p.drawString(628, 1343, row["COUNTRY"].decode("cp1252"))
        p.drawString(792, 1201, row["LOCATION"].decode("cp1252"))
        p.drawString(592, 1085, row["ACTIVITY"].decode("cp1252"))
        stylesheet = styles.getSampleStyleSheet()
        style = stylesheet['Normal']
        style.fontName = 'Canaro'
        style.fontSize = 50
        style.leading = 60
        pr = Paragraph(row["ABOUT ACTIVITY"].decode("cp1252"), style)
        wd, ht = pr.wrap (1200, 600)
        pr.drawOn(p, 229, 536 - ht)
        p.showPage()
        p.drawImage(urlBase%8,0,0)
        pr = Paragraph(row["SPECIFICATIONS"].decode("cp1252"), style)
        wd, ht = pr.wrap (1500, 600)
        pr.drawOn(p, 100, 1865 - ht)
        pr = Paragraph(row["INFORMATION ABOUT YOUR KID"].decode("cp1252"), style)
        wd, ht = pr.wrap (1450, 600)
        pr.drawOn(p, 100, 1562 - ht)
        p.showPage()
        p.drawImage(urlBase%9,0,0)
        p.showPage()
        p.drawImage(urlBase%10,0,0)
        p.save()
        pdf = buffer.getvalue()
        buffer.close()
        #response.write(pdf)
        #return response
        name = row["TRAINEE"].decode("cp1252").replace('/', '-')
        filepath = u'/home/camilo/public/bookletsFinalesFuera/%s.pdf' % name
        filepath = filepath.encode('utf-8')
        f = open(filepath, 'wb')
        f.write(pdf)
        f.close()
        break
        
    return response

def crearBookletsAfuera(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="diplomas.pdf"'
    datos = open('/home/camilo/public/papalito/graduados.csv', 'r')
    reader = csv.DictReader(datos)
    actual = 0
    ultimoError = 0 
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=(1700,2200))
    ttfFile = os.path.join('/home/camilo/public/papalito', 'ThrowMyHandsUpintheAirBold.ttf')
    pdfmetrics.registerFont(TTFont("Canaro", ttfFile))
    urlBase = '/home/camilo/public/papalito/diplomas papalito1-1.png'
    for row in reader:
        if actual < ultimoError:
            actual += 1
            continue
        actual += 1
        p.drawImage(urlBase, 0, 0)
        p.setFont('Canaro', 38)
        p.drawCentredString(838, 1816, row['Graduado1'])
        p.drawCentredString(838, 716, row['Graduado2'])
        p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
