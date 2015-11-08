# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cluster',
            fields=[
                ('nombre', models.CharField(max_length=16, serialize=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='LC',
            fields=[
                ('nombre', models.CharField(max_length=32, serialize=False, primary_key=True)),
                ('logo', models.ImageField(null=True, upload_to=b'')),
                ('cluster', models.ForeignKey(related_name='lcs', to='bam.Cluster', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Puntajes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('OGCDP', models.PositiveSmallIntegerField(default=0)),
                ('IGCDP', models.PositiveSmallIntegerField(default=0)),
                ('ip_IGCDP', models.PositiveSmallIntegerField(default=0)),
                ('ma_IGCDP', models.PositiveSmallIntegerField(default=0)),
                ('re_IGCDP', models.PositiveSmallIntegerField(default=0)),
                ('bonus_IGCDP', models.PositiveSmallIntegerField(default=0)),
                ('OGIP', models.PositiveSmallIntegerField(default=0)),
                ('IGIP', models.PositiveSmallIntegerField(default=0)),
                ('lc', models.ForeignKey(to='bam.LC')),
            ],
        ),
        migrations.CreateModel(
            name='Semana',
            fields=[
                ('id', models.PositiveSmallIntegerField(serialize=False, primary_key=True)),
            ],
        ),
        migrations.AddField(
            model_name='puntajes',
            name='semana',
            field=models.ForeignKey(to='bam.Semana'),
        ),
        migrations.AddField(
            model_name='lc',
            name='semana',
            field=models.ManyToManyField(related_name='lcs', through='bam.Puntajes', to='bam.Semana'),
        ),
        migrations.AlterUniqueTogether(
            name='puntajes',
            unique_together=set([('lc', 'semana')]),
        ),
    ]
