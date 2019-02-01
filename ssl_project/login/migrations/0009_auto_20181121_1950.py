# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0008_enc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enc',
            name='schema',
            field=models.CharField(max_length=100),
        ),
    ]
