# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fileManager', '0007_trainee_fecha_creacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainee',
            name='full_name',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='trainee',
            name='lc_host',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
