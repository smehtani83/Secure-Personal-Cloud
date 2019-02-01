# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0012_rec'),
    ]

    operations = [
        migrations.AddField(
            model_name='rec',
            name='file',
            field=models.CharField(default=52, max_length=100),
            preserve_default=False,
        ),
    ]
