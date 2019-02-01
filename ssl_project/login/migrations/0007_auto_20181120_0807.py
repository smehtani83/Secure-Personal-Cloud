# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_sync'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sync',
            name='user',
        ),
        migrations.DeleteModel(
            name='Sync',
        ),
    ]
