# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='file_link',
        ),
        migrations.AddField(
            model_name='file',
            name='file',
            field=models.BinaryField(blank=True),
        ),
    ]
