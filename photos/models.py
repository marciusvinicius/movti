# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Photo(models.Model):
    """
    Mapping photo fields
    """
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    content = models.TextField(null=True)

    def __str__(self):
        return self.name
