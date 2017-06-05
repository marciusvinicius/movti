# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from datetime import datetime
from django.conf import settings
from django.db import models


class Photo(models.Model):
    """
    Mapping photo fields
    """
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    content = models.TextField(null=True, blank=True)
    upload = models.ImageField()

    def __str__(self):
        return self.name
