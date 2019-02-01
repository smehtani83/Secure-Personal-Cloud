# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0009_auto_20181121_1950'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='md5sum',
            field=models.CharField(default=1234567899999990, max_length=100),
            preserve_default=False,
        ),
    ]
