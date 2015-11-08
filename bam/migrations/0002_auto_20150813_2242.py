# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bam', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='puntajes',
            name='bonus_IGIP',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='puntajes',
            name='bonus_OGCDP',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='puntajes',
            name='bonus_OGIP',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='puntajes',
            name='ip_IGIP',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='puntajes',
            name='ip_OGCDP',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='puntajes',
            name='ip_OGIP',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='puntajes',
            name='ma_IGIP',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='puntajes',
            name='ma_OGCDP',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='puntajes',
            name='ma_OGIP',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='puntajes',
            name='re_IGIP',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='puntajes',
            name='re_OGCDP',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='puntajes',
            name='re_OGIP',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
