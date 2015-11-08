# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.db import models

from django_countries.fields import CountryField

def upload_prefix(instance, name):
    return u"%s/%s/%s" % (instance.empresa.nombre, instance.id, name)

class Empresa(models.Model):
    nombre = models.CharField(max_length=64)
    direccion = models.CharField(max_length=128)
    ciudad = models.CharField(max_length=32)
    departamento = models.CharField(max_length=32)
    telefono = models.CharField(max_length=32)
    NIT = models.CharField(max_length=32, blank=True, null=True, help_text=_(u"El NIT de la empresa"))
    salario = models.IntegerField(default = 0, help_text=_(u"El salario que le da la empresa a los practicantes"))
    nombre_representante = models.CharField(max_length=128, default="SIN ASIGNAR")
    cargo_representante = models.CharField(max_length=64, default="SIN ASIGNAR")
    correo_representante = models.EmailField(null=True)
    tn_id = models.PositiveIntegerField(null=True)

    def __unicode__(self):
        return self.nombre

class Perfil(models.Model):
    GENDER_CHOICES = (
        ('M', _("Masculino")),
        ('F', _("Femenino")),
        ('O', _("Otro")),
    )
    genero = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, verbose_name=_(u"Género")) 
    user = models.OneToOneField(User, null=True, related_name="%(class)s")
    empresa = models.ForeignKey(Empresa, related_name="%(class)ss", verbose_name=_(u"Empresa"), help_text=_(u"Compañía para la cual trabajarará el trainee"))
    country = CountryField(null=True, help_text=_(u"País de origen"), verbose_name=_(u"País"))
    num_pasaporte = models.CharField(null=True, max_length=64, help_text=_(u"Tu número de pasaporte"), verbose_name=_(u"Número de pasaporte"))
    telefono = models.CharField(null=True, verbose_name=_(u"Teléfono"), help_text=_(u"Número telefónico"), max_length=32)
    photo = models.ImageField(null=True, blank=True)
    def __unicode__(self):
        if self.user:
            return self.user.first_name
        return "noUser" + self.empresa.nombre
    def upload_prefix(self):
        return "%s/%s/" % self.id, self.empresa.nombre
    class Meta:
        abstract = True

class Trainee(Perfil):
    code = models.CharField(max_length=16, null=True, unique=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    grupo = models.CharField(max_length=32, blank=False, null=False, default="Grupo 1")
    full_name = models.CharField(max_length=128, null=True)
    curriculum_vitae = models.FileField(upload_to=upload_prefix, null=True, help_text=_("Hoja de vida"))
    estado = models.NullBooleanField(null=True, default=None, help_text="Elija la casilla adecuada de acuerdo a si desea aceptar o rechazar a este aplicante en base a su hoja de vida")
    confirmado=models.BooleanField(default=False, help_text=_(u"Este campo muestra si el trainee ya ha confirmado su participación, llenando el formulario de confirmación con su pasaporte, entre otros datos"))
    lc_host = models.CharField(max_length=64, null=True)
    documentos_hechos = models.BooleanField(default=False, help_text=u"Este campo muestra si el memodeal del trainee ha sido generado y si se le ha enviado un correo pidiéndole más detalles")
    pasaporte = models.ImageField(null=True, verbose_name=_("Foto del pasaporte"), help_text=_("Una imagen escaneada del pasaporte. Las fotos no son permitidas"))
    fecha_expedicion_pasaporte = models.DateField(null=True, verbose_name=_(u"Fecha de expedición del pasaporte"), help_text=_(u"Fecha en la cual se expidió el pasaporte"))
    fecha_expiracion_pasaporte = models.DateField(null=True, verbose_name=_(u"Fecha de expiración del pasaporte"), help_text=_("Fecha en la cual el pasaporte va a expirar"))
    memodeal = models.FileField(upload_to = upload_prefix, null=True)
    memodeal_firmado = models.FileField(upload_to = upload_prefix, null=True)
    ep_id = models.PositiveIntegerField(null=True, help_text=_("La id del trainee"))
    tn_id = models.PositiveIntegerField(null=True, help_text=_("La id de la oportunidad"))
    fecha_inicio_practica = models.DateField(null=True, verbose_name=_(u"Fecha de inicio"), help_text="La fecha cuando este practicante va a comenzar a trabajar para la empresa")
    fecha_fin_practica = models.DateField(null=True, verbose_name=_(u"Fecha final"), help_text=u"Fecha cuando el practicante finalizará su experiencia dentro de la empresa")
    acceptance_note = models.FileField(null=True, upload_to = upload_prefix)
    acceptance_note_firmada = models.FileField(null=True, upload_to = upload_prefix)
    organization_acceptance_note = models.FileField(null=True, upload_to = upload_prefix)
    organization_acceptance_note_firmada = models.FileField(null=True, upload_to = upload_prefix)
    seguro_internacional = models.FileField(null=True, upload_to = upload_prefix)
    certificado_cuenta_bancaria = models.FileField(null=True, upload_to = upload_prefix)
    carta_mercosur = models.FileField(null=True, upload_to = upload_prefix)
    eps = models.FileField(null=True, upload_to = upload_prefix)
    arl = models.FileField(null=True, upload_to = upload_prefix)
    otros = models.FileField(null=True, upload_to = upload_prefix)
    def __unicode__(self):
        if self.full_name:
            return self.full_name
        else:
            return "%s %s" % (self.user.first_name, self.user.last_name)

class Empresario(Perfil):
    pass

class Admin(Perfil):
    pass    
# Create your models here.
