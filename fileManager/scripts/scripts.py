# -*- coding: utf-8 -*-
from django.core.files import File
from django.core.files.base import ContentFile
from django.contrib.auth.models import User

from fileManager.models import Trainee, Empresa

import csv
import urllib2
import random
import string

reader = None


def cargarTrainees(uploadedFile, empresa, grupo):
    repetidos = list()
    cv_desactualizado = list()
    exitosos = list()
    no_cv = list()
    otros = list()
    rawfile = uploadedFile.file
    reader = csv.DictReader(rawfile, delimiter=';')
    for row in reader:
        nombre = row["Applicant Name"].decode(encoding="utf-8")
        try:
            tn_id = row["Opportunity"].rsplit('/',1)[1]
            ep_id = row["Profile"].rsplit('/',1)[1]
        except IndexError:
            otros.append(nombre)
            continue
        email = row["Applicant Email"].lower()
        lc_host = row["Applicant Home LC"].decode(encoding="latin-1")
        obj_empresa = Empresa.objects.get(pk=empresa)
        trainee = Trainee(id=ep_id, ep_id=ep_id, tn_id=tn_id, lc_host=lc_host, empresa=obj_empresa, grupo=grupo) 
        code = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))
        trainee.code = code
        try:
            cv = urllib2.urlopen(row["CV"])
            ext = row["CV"].split(".")[-1]
        except urllib2.HTTPError:
            cv_desactualizado.append(nombre)
            continue
        except ValueError:
            no_cv.append(nombre)
            continue
        save_name=u"cv_%s.%s" % (nombre, ext)
        trainee.curriculum_vitae.save(save_name.encode('ascii', 'ignore'), ContentFile(cv.read()), save=False)
        try:
            user = User.objects.create_user(username=email.split("@")[0], password=code)
        except:
            repetidos.append(nombre)
            continue
        trainee.full_name=nombre
        user.email = email
        user.is_active = False
        user.save()
        trainee.user=user
        trainee.save()
        exitosos.append(nombre)
    return {"exitosos":exitosos, "cv_desactualizado":cv_desactualizado, "repetidos":repetidos, "no_cv":no_cv, "otros":otros}
