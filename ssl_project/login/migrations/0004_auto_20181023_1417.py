# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_auto_20181022_1828'),
    ]

    operations = [
        migrations.RenameField(
            model_name='file',
            old_name='file',
            new_name='file_file',
        ),
    ]
