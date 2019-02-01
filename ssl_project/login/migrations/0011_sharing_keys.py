# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('login', '0010_file_md5sum'),
    ]

    operations = [
        migrations.CreateModel(
            name='sharing_keys',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('n', models.CharField(max_length=1000)),
                ('e', models.CharField(max_length=1000)),
                ('d', models.CharField(max_length=1000)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
