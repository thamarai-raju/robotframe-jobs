# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
class Testdata(models.Model):
    testsuite = models.CharField(max_length=100)
    testfile  = models.CharField(max_length=200)
    testcase  = models.TextField()
    tag = models.ManyToManyField('Tag')