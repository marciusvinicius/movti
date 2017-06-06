# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Photo


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """
    Administration Register
    """
    fields = ('name', 'description', 'upload', 'content', 'image_tag')
    readonly_fields = ('content', 'image_tag')
