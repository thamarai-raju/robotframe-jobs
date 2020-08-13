# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-08-13 18:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Testdata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testsuite', models.CharField(max_length=100)),
                ('testfile', models.CharField(max_length=200)),
                ('testcase', models.TextField()),
                ('tag', models.ManyToManyField(to='robotjobs.Tag')),
            ],
        ),
    ]
