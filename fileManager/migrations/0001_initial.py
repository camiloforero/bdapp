# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import fileManager.models
import django_countries.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('genero', models.CharField(max_length=1, null=True, verbose_name='G\xe9nero', choices=[(b'M', 'Masculino'), (b'F', 'Femenino'), (b'O', 'Otro')])),
                ('country', django_countries.fields.CountryField(help_text='Pa\xeds de origen', max_length=2, null=True, verbose_name='Pa\xeds')),
                ('num_pasaporte', models.CharField(help_text='Tu n\xfamero de pasaporte', max_length=64, null=True, verbose_name='N\xfamero de pasaporte')),
                ('a', models.CharField(max_length=2, null=True)),
                ('telefono', models.CharField(help_text='N\xfamero telef\xf3nico', max_length=32, null=True, verbose_name='Tel\xe9fono')),
                ('photo', models.ImageField(null=True, upload_to=b'', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=64)),
                ('direccion', models.CharField(max_length=128)),
                ('ciudad', models.CharField(max_length=32)),
                ('departamento', models.CharField(max_length=32)),
                ('telefono', models.CharField(max_length=32)),
                ('NIT', models.CharField(help_text='El NIT de la empresa', max_length=32, null=True, blank=True)),
                ('salario', models.IntegerField(default=0, help_text='El salario que le da la empresa a los practicantes')),
                ('nombre_representante', models.CharField(default=b'SIN ASIGNAR', max_length=128)),
                ('cargo_representante', models.CharField(default=b'SIN ASIGNAR', max_length=64)),
                ('correo_representante', models.EmailField(max_length=254, null=True)),
                ('tn_id', models.PositiveSmallIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Empresario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('genero', models.CharField(max_length=1, null=True, verbose_name='G\xe9nero', choices=[(b'M', 'Masculino'), (b'F', 'Femenino'), (b'O', 'Otro')])),
                ('country', django_countries.fields.CountryField(help_text='Pa\xeds de origen', max_length=2, null=True, verbose_name='Pa\xeds')),
                ('num_pasaporte', models.CharField(help_text='Tu n\xfamero de pasaporte', max_length=64, null=True, verbose_name='N\xfamero de pasaporte')),
                ('a', models.CharField(max_length=2, null=True)),
                ('telefono', models.CharField(help_text='N\xfamero telef\xf3nico', max_length=32, null=True, verbose_name='Tel\xe9fono')),
                ('photo', models.ImageField(null=True, upload_to=b'', blank=True)),
                ('empresa', models.ForeignKey(related_name='empresarios', verbose_name='Empresa', to='fileManager.Empresa', help_text='Compa\xf1\xeda para la cual trabajarar\xe1 el trainee')),
                ('user', models.OneToOneField(related_name='empresario', null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Trainee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('genero', models.CharField(max_length=1, null=True, verbose_name='G\xe9nero', choices=[(b'M', 'Masculino'), (b'F', 'Femenino'), (b'O', 'Otro')])),
                ('country', django_countries.fields.CountryField(help_text='Pa\xeds de origen', max_length=2, null=True, verbose_name='Pa\xeds')),
                ('num_pasaporte', models.CharField(help_text='Tu n\xfamero de pasaporte', max_length=64, null=True, verbose_name='N\xfamero de pasaporte')),
                ('a', models.CharField(max_length=2, null=True)),
                ('telefono', models.CharField(help_text='N\xfamero telef\xf3nico', max_length=32, null=True, verbose_name='Tel\xe9fono')),
                ('photo', models.ImageField(null=True, upload_to=b'', blank=True)),
                ('code', models.CharField(max_length=16, unique=True, null=True)),
                ('full_name', models.CharField(max_length=256, null=True)),
                ('curriculum_vitae', models.FileField(help_text='Hoja de vida', null=True, upload_to=fileManager.models.upload_prefix)),
                ('estado', models.NullBooleanField(default=None, help_text=b'Elija la casilla adecuada de acuerdo a si desea aceptar o rechazar a este aplicante en base a su hoja de vida')),
                ('lc_host', models.CharField(max_length=32, null=True)),
                ('correo_enviado', models.BooleanField(default=False, help_text='Este campo muestra si el memodeal del trainee ha sido generado y si se le ha enviado un correo pidi\xe9ndole m\xe1s detalles')),
                ('pasaporte', models.ImageField(help_text='Una imagen escaneada del pasaporte. Las fotos no son permitidas', upload_to=b'', null=True, verbose_name='Foto del pasaporte')),
                ('fecha_expedicion_pasaporte', models.DateField(help_text='Fecha en la cual se expidi\xf3 el pasaporte', null=True, verbose_name='Fecha de expedici\xf3n del pasaporte')),
                ('fecha_expiracion_pasaporte', models.DateField(help_text='Fecha en la cual el pasaporte va a expirar', null=True, verbose_name='Fecha de expiraci\xf3n del pasaporte')),
                ('memodeal', models.FileField(null=True, upload_to=fileManager.models.upload_prefix)),
                ('memodeal_firmado', models.FileField(null=True, upload_to=fileManager.models.upload_prefix)),
                ('ep_id', models.PositiveIntegerField(help_text='La id del trainee', null=True)),
                ('tn_id', models.PositiveIntegerField(help_text='La id de la oportunidad', null=True)),
                ('fecha_inicio_practica', models.DateField(help_text=b'La fecha cuando este practicante va a comenzar a trabajar para la empresa', null=True, verbose_name='Fecha de inicio')),
                ('fecha_fin_practica', models.DateField(help_text='Fecha cuando el practicante finalizar\xe1 su experiencia dentro de la empresa', null=True, verbose_name='Fecha final')),
                ('carta_1', models.FileField(null=True, upload_to=fileManager.models.upload_prefix)),
                ('carta_1_firmada', models.FileField(null=True, upload_to=fileManager.models.upload_prefix)),
                ('carta_2', models.FileField(null=True, upload_to=fileManager.models.upload_prefix)),
                ('carta_2_firmada', models.FileField(null=True, upload_to=fileManager.models.upload_prefix)),
                ('seguro_internacional', models.FileField(null=True, upload_to=b'')),
                ('eps', models.FileField(null=True, upload_to=b'')),
                ('arl', models.FileField(null=True, upload_to=b'')),
                ('otros', models.FileField(null=True, upload_to=b'')),
                ('empresa', models.ForeignKey(related_name='trainees', verbose_name='Empresa', to='fileManager.Empresa', help_text='Compa\xf1\xeda para la cual trabajarar\xe1 el trainee')),
                ('user', models.OneToOneField(related_name='trainee', null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='admin',
            name='empresa',
            field=models.ForeignKey(related_name='admins', verbose_name='Empresa', to='fileManager.Empresa', help_text='Compa\xf1\xeda para la cual trabajarar\xe1 el trainee'),
        ),
        migrations.AddField(
            model_name='admin',
            name='user',
            field=models.OneToOneField(related_name='admin', null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
