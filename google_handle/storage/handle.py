
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import mimetypes

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from google.appengine.ext.blobstore.blobstore import create_gs_key



import cloudstorage as gcs


class GoogleCloudStorage(Storage):
    """
    Creating a Django Storage for google cloud
    """
    def __init__(self, location=None, base_url=None):
        if location is None:
            location = settings.GOOGLE_CLOUD_STORAGE_BUCKET
        self.location = location
        if base_url is None:
            base_url = settings.GOOGLE_CLOUD_STORAGE_URL
        self.base_url = base_url

    def exists(self, name):
        return True if self.stat_file(name) else False

    #@TODO:OPen with diferent file mode
    def _open(self, name, file_mode='rb'):
        filename = "/%s/%s" % (self.location, name)
        gcs_file = gcs.open(filename, mode="r")
        content_file = ContentFile(gcs_file.read())
        gcs_file.close()
        return content_file

    def _save(self, name, content, *args, **kwargs):
        filename = "/%s/%s" % (self.location, name)
        filename = os.path.normpath(filename)
        file_type, _ = mimetypes.guess_type(name)
        gss_file = gcs.open(
            filename, mode='w', content_type=file_type,
            options={
                'x-goog-acl': 'public-read',
                'cache-control': settings.GOOGLE_CLOUD_STORAGE_DEFAULT_CACHE_CONTROL
            }
        )
        content.open()
        gss_file.write(content.read())
        content.close()
        gss_file.close()
        return name

    def size(self, name):
        """
        Return the size
        """
        stats = self.stat_file(name)
        return stats.st_size

    def url(self, name):
        """
        Return the URL Based on debug
        """
        if settings.ENVTYPE == "GOOGLE":
            filename = "/gs/%(location)s/%(name)s" % {
                "location": self.location,
                "name": name,
            }
            key = create_gs_key(filename)
            return "http://localhost:8000/blobstore/blob/%s?%s" % (key, "display=inline")
        return "/%s/%s" % (self.location, name)

    def stat_file(self, name):
        """
        Return the Stat
        """
        filename = "/%s/%s" % (self.location, name)
        try:
            return gcs.stat(filename)
        except Exception:
            return None
