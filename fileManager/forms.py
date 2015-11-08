# -*- coding: utf-8 -*-
from django import forms
from django.forms import Form, ModelForm, DateField
from django.forms.models import modelformset_factory
from django.forms.widgets import HiddenInput

from datetimewidget.widgets import DateTimeWidget, DateWidget
from fileManager.models import Trainee, Empresa

class InscriptionForm(ModelForm):
    """Esta forma maneja la inscripción de los trainees a la plataforma. Incluye algunos de sus datos básicos y sus hojas de vida."""
    class Meta:
        model = Trainee
        fields = ['genero', 'id', 'country', 'empresa', 'curriculum_vitae']

class AcceptanceForm(ModelForm):
    """Esta forma maneja la inscripción de los trainees a la plataforma. Incluye algunos de sus datos básicos y sus hojas de vida."""
    fecha_inicio_practica = DateField(input_formats=['%d/%m/%Y'], widget=DateWidget(bootstrap_version=3, usel10n=True))
    fecha_fin_practica = DateField(input_formats=['%d/%m/%Y'], widget=DateWidget(bootstrap_version=3, usel10n=True))
    class Meta:
        model = Trainee
        fields = ['id', 'fecha_inicio_practica', 'fecha_fin_practica']
        widgets = {'id':HiddenInput(), 'fecha_inicio_practica':DateWidget(bootstrap_version=3, usel10n=True), 'fecha_fin_practica':DateWidget(bootstrap_version=3, usel10n=True)}

class CartasForm(ModelForm):
    """Esta forma maneja las cartas de aceptación firmadas que son subidas por el representante de la empresa, para continuar con el proceso de legalización y visado"""
    class Meta:
        model = Trainee
        fields = ['acceptance_note_firmada', 'organization_acceptance_note_firmada']

class ConfirmationForm(ModelForm):
    """Esta forma maneja la inscripción de los trainees a la plataforma. Incluye algunos de sus datos básicos y sus hojas de vida."""
    code2 = forms.CharField(max_length=16, required=True, label="Code")
    fecha_expedicion_pasaporte = DateField(input_formats=['%d/%m/%Y'], label="Issue date", widget=DateWidget(bootstrap_version=3, usel10n=True))
    fecha_expiracion_pasaporte = DateField(input_formats=['%d/%m/%Y'], label="Expiration date", widget=DateWidget(bootstrap_version=3, usel10n=True))
    class Meta:
        model = Trainee
        fields = ['code2', 'pasaporte', 'num_pasaporte', 'fecha_expedicion_pasaporte', 'fecha_expiracion_pasaporte', 'genero', 'country', 'telefono']
        widgets = {'fecha_expedicion_pasaporte':DateWidget(bootstrap_version=3, usel10n=True), 'fecha_expiracion_pasaporte':DateWidget(bootstrap_version=3, usel10n=True)}

class UserForm(Form):
    first_name = forms.CharField(max_length=64, required=True, label="First name")
    last_name = forms.CharField(max_length=64, required=True, label="Last name")
    email = forms.EmailField(required=True, label="Email")

TraineeFormSet = modelformset_factory(Trainee, fields=('id',), widgets={'id':HiddenInput()}, extra=0)


class CSVTraineesForm(Form):
    empresa = forms.ModelChoiceField(Empresa.objects.all())
    csv = forms.FileField()
    grupo = forms.CharField()

