# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_auto_20181023_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='file_address',
            field=models.CharField(default='./', max_length=1000),
            preserve_default=False,
        ),
    ]
