# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import fileManager.models


class Migration(migrations.Migration):

    dependencies = [
        ('fileManager', '0009_trainee_grupo'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainee',
            name='carta_mercosur',
            field=models.FileField(null=True, upload_to=fileManager.models.upload_prefix),
        ),
        migrations.AddField(
            model_name='trainee',
            name='certificado_cuenta_bancaria',
            field=models.FileField(null=True, upload_to=fileManager.models.upload_prefix),
        ),
        migrations.AlterField(
            model_name='trainee',
            name='arl',
            field=models.FileField(null=True, upload_to=fileManager.models.upload_prefix),
        ),
        migrations.AlterField(
            model_name='trainee',
            name='eps',
            field=models.FileField(null=True, upload_to=fileManager.models.upload_prefix),
        ),
        migrations.AlterField(
            model_name='trainee',
            name='otros',
            field=models.FileField(null=True, upload_to=fileManager.models.upload_prefix),
        ),
        migrations.AlterField(
            model_name='trainee',
            name='seguro_internacional',
            field=models.FileField(null=True, upload_to=fileManager.models.upload_prefix),
        ),
    ]
