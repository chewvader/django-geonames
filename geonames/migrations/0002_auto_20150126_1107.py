# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geonames', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alternate',
            old_name='geonameid',
            new_name='geoname',
        ),
    ]
