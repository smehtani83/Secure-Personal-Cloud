# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0013_rec_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Id',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('usera', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Shared_File',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('usera', models.IntegerField()),
                ('userb', models.IntegerField()),
                ('file_type', models.CharField(max_length=10)),
                ('file_name', models.CharField(max_length=100)),
                ('file_file', models.FileField(upload_to='')),
                ('file_address', models.CharField(max_length=1000)),
                ('md5sum', models.CharField(max_length=100)),
            ],
        ),
    ]
