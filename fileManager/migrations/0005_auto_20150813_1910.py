# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fileManager', '0004_auto_20150813_1905'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trainee',
            old_name='carta_1',
            new_name='acceptance_note',
        ),
        migrations.RenameField(
            model_name='trainee',
            old_name='carta_1_firmada',
            new_name='acceptance_note_firmada',
        ),
    ]
