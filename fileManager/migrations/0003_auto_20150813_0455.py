# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fileManager', '0002_auto_20150812_1813'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='admin',
            name='a',
        ),
        migrations.RemoveField(
            model_name='empresario',
            name='a',
        ),
        migrations.RemoveField(
            model_name='trainee',
            name='a',
        ),
    ]
