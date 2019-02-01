# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('login', '0011_sharing_keys'),
    ]

    operations = [
        migrations.CreateModel(
            name='rec',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('usera', models.CharField(max_length=100)),
                ('sofbwa', models.CharField(max_length=1000)),
                ('userb', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
