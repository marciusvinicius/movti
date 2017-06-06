# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.db import models

from google_handle.vision.handle import get_content


def upload_to(self):
    pass

class Photo(models.Model):
    """
    Mapping photo fields
    """
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    content = models.TextField(null=True, blank=True)
    upload = models.ImageField(upload_to="file")

    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        super(Photo, self).save(*args, **kwargs)
        if not self.content:
            self.content = get_content(self)
