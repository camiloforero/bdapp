# -*- coding: utf-8 -*-
from django.core.files.uploadedfile import UploadedFile
from django.core.mail import send_mail
from django.utils import timezone, translation
from django.template.response import TemplateResponse
from django.template.loader import render_to_string
from django.views.generic import ListView
from django.views.generic.edit import UpdateView

from fileManager.models import Trainee
from fileManager.forms import TraineeFormSet, CSVTraineesForm
from fileManager.scripts import scripts
from fileManager import aux

from datetime import date, timedelta
from calendar import TimeEncoding, month_name

import locale

def get_month_name(month_no, locale):
    """Esta función permite obtener el nombre de un mes traducido a un idioma en especial, indispensable para generar el memodeal"""
    with TimeEncoding(locale) as encoding:
        s = month_name[month_no]
        if encoding is not None:
            s = s.decode(encoding)
        return s


def crear_documentos(request):
    if request.POST:
        formset = TraineeFormSet(request.POST)
        for form in formset.forms:
            trainee = form.save(commit=False)
            if trainee:
                today = timezone.now()
                inicio = trainee.fecha_inicio_practica
                fin = trainee.fecha_fin_practica
                duracion = fin - inicio
                datos = {
                    "full_name": trainee,
                    "email": trainee.user.email,
                    "telefono": trainee.telefono,
                    "tn_id": trainee.empresa.tn_id,
                    "ep_id": trainee.ep_id,
                    "fecha_actual": today.strftime("%d-%m-%Y"),
                    "empresa": trainee.empresa.nombre,
                    "direccion_empresa": trainee.empresa.direccion,
                    "ciudad_empresa": trainee.empresa.ciudad,
                    "departamento_empresa": trainee.empresa.departamento,
                    "telefono_empresa": trainee.empresa.telefono,
                    "fecha_inicio": inicio.strftime("%d-%m-%Y"),
                    "fecha_fin": fin.strftime("%d-%m-%Y"),
                    "subsidio": trainee.empresa.salario,
                    "num_pasaporte": trainee.num_pasaporte,
                    "id_issue_date": trainee.fecha_expedicion_pasaporte,
                    "id_expiration_date": trainee.fecha_expiracion_pasaporte,
                    "nombre_representante": trainee.empresa.nombre_representante,
                    "cargo_representante": trainee.empresa.cargo_representante,
                    "correo_representante": trainee.empresa.correo_representante,
                }
                datos["num_semanas"] = duracion.days/7
                translation.activate('es')
                locale.setlocale(locale.LC_TIME, "es_CO.utf8")
                datos["pais"] = unicode(trainee.country.name).encode('utf-8')
                datos["fecha"]= today.strftime("%d de %B del %Y").encode('utf-8')
                datos["fecha_inicio_espanol"]= inicio.strftime("%d de %B del %Y").encode('utf-8')
                datos["fecha_fin_espanol"]= fin.strftime("%d de %B del %Y").encode('utf-8')
                datos["genero"]= trainee.genero
                locale.setlocale(locale.LC_TIME, "en_US.utf8")
                translation.activate('en')
                datos["country"]= unicode(trainee.country.name).encode('utf-8')
                datos["date"]= today.strftime("%d of %B, %Y").encode('utf-8')
                translation.deactivate()
                pdf = aux.generatePdf("memodeal.odt", datos)
                pdfFile = UploadedFile(pdf)
                trainee.memodeal.save("memodeal_%s.pdf" % trainee.tn_id, pdfFile)
                pdf = aux.generatePdf("acceptance_note.odt", datos)
                pdfFile = UploadedFile(pdf)
                trainee.acceptance_note.save("acceptance_note_%s.pdf" % trainee.tn_id, pdfFile)
                pdf = aux.generatePdf("organization_acceptance_note.odt", datos)
                pdfFile = UploadedFile(pdf)
                trainee.organization_acceptance_note.save("organization_acceptance_note_%s.pdf" % trainee.tn_id, pdfFile)
                pdf = aux.generatePdf("carta_mercosur.odt", datos)
                pdfFile = UploadedFile(pdf)
                trainee.carta_mercosur.save("carta_mercosur_%s.pdf" % trainee.tn_id, pdfFile)
                pdf = aux.generatePdf("certificado_cuenta_bancaria.odt", datos)
                pdfFile = UploadedFile(pdf)
                trainee.certificado_cuenta_bancaria.save("certificado_cuenta_bancaria_%s.pdf" % trainee.tn_id, pdfFile)
		trainee.documentos_hechos = True
                trainee.save()
        context = {'mensaje': "Se han generado los memodeals exitosamente"}
        return TemplateResponse(request, "admin/fileManager/crear_memodeals_done.html", context)
    else:
        trainees = Trainee.objects.filter(confirmado=True, documentos_hechos=False) 
        formset = TraineeFormSet(queryset=trainees)
        context = {"trainees": trainees, "formset":formset,} 
        return TemplateResponse(request, "admin/fileManager/crear_memodeals.html", context)

def subir_trainees(request):
    if request.POST:
        form = CSVTraineesForm(request.POST, request.FILES)
        if form.is_valid():
            csv = request.FILES['csv']
            context = scripts.cargarTrainees(csv, request.POST["empresa"], request.POST["grupo"])
            return TemplateResponse(request, "admin/resultado_subir_trainees.html", context)

    else:
        forms = [CSVTraineesForm(),]
        context = {"forms":forms}
        return TemplateResponse(request, "admin/admin_form.html", context)

class MostrarSubirPapeles(ListView):
    queryset = Trainee.objects.filter(*aux.QDICT['por_legalizar'])
    template_name = 'admin/subir_papeles.html'

class SubirPapeles(UpdateView):
    model = Trainee
    fields = ['seguro_internacional', 'eps', 'arl']
    template_name = 'admin/admin_single_form.html'
    context_object_name = 'form' 
