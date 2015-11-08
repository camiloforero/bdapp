# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bam', '0002_auto_20150813_2242'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='puntajes',
            name='re_IGCDP',
        ),
        migrations.RemoveField(
            model_name='puntajes',
            name='re_IGIP',
        ),
        migrations.RemoveField(
            model_name='puntajes',
            name='re_OGCDP',
        ),
        migrations.RemoveField(
            model_name='puntajes',
            name='re_OGIP',
        ),
    ]
