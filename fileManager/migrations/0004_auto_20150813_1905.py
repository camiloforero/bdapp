# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fileManager', '0003_auto_20150813_0455'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trainee',
            old_name='correo_enviado',
            new_name='documentos_hechos',
        ),
        migrations.AddField(
            model_name='trainee',
            name='confirmado',
            field=models.BooleanField(default=False, help_text='Este campo muestra si el trainee ya ha confirmado su participaci\xf3n, llenando el formulario de confirmaci\xf3n con su pasaporte, entre otros datos'),
        ),
    ]
