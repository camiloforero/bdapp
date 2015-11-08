# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fileManager', '0008_auto_20150914_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainee',
            name='grupo',
            field=models.CharField(default=b'Grupo 1', max_length=32),
        ),
    ]
