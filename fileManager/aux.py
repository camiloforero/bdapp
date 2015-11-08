# -*- coding: utf-8 -*-

from django.template import Context
from django.db.models import Q
from webodt.converters import converter


import os
import subprocess
import webodt

def generatePdf(name, context):
    """Esta función genera un PDF a partir de un documento en formato ODT, con las variables asignadas, y un diccionario que asocia las variables con sus valores"""
    template = webodt.ODFTemplate(name)
    document = template.render(Context(context), delete_on_close=False)
    oldenviron = os.environ['HOME']
    os.environ['HOME'] = "/tmp"
    returncode = subprocess.call(["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", "/tmp", document.name])
    print "Return code: %s " % str(returncode)
    filename, file_extension = os.path.splitext(document.name)
    pdf = open(filename + ".pdf")
    os.environ['HOME'] = oldenviron
    return pdf

QDICT = { 
    "cartas_firmadas": (~Q(acceptance_note=''), ~Q(acceptance_note_firmada='')),
    "por_legalizar": (~Q(acceptance_note=''), ~Q(acceptance_note_firmada=''), Q(seguro_internacional='')),
    "aceptados": (Q(estado=True),),
    "cartas_generadas": (~Q(acceptance_note=''), Q(acceptance_note_firmada='')),
    "por_aceptar": (Q(estado=None),),
    }
