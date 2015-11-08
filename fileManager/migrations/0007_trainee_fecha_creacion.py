# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('fileManager', '0006_auto_20150813_2059'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainee',
            name='fecha_creacion',
            field=models.DateField(default=datetime.datetime(2015, 9, 14, 4, 50, 15, 192509, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
