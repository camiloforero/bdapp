# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fileManager', '0005_auto_20150813_1910'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trainee',
            old_name='carta_2',
            new_name='organization_acceptance_note',
        ),
        migrations.RenameField(
            model_name='trainee',
            old_name='carta_2_firmada',
            new_name='organization_acceptance_note_firmada',
        ),
    ]
