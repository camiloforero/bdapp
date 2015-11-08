# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fileManager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresa',
            name='tn_id',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
