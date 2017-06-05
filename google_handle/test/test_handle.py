# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.conf import settings
from google_handle.storage.google_cloud import GoogleCloudStorage

import mock


class GoogleStorageTestCase(TestCase):

    def test_create_init(self):
        storage = GoogleCloudStorage()
        self.asertEqual(storage.location, settings.GOOGLE_CLOUD_STORAGE_BUCKET)
        self.asertEqual(storage.base_url, settings.GOOGLE_CLOUD_STORAGE_URL)

    @mock.path("google_handle.storage.google_clound.ContentFile")
    @mock.path("google_handle.storage.google_clound.gcs")
    def test_on_open(self, gcs, ContentFile):
        storage = GoogleCloudStorage()
        storage.open("test.png")
        file_name = "%s/%s" % (
            settings.GOOGLE_CLOUD_STORAGE_URL,
            "test.png")
        gcs.open.assert_called_with(file_name, "r")
        gcs_file = mock.Mock()
        gcs.open.return_value = gcs_file
        gcs_file.read.assert_called()

    @mock.path("google_handle.storage.google_clound.gcs")
    def test_on_save(self, gcs):
        storage = GoogleCloudStorage()
        content = mock.Mock()
        storage.save(name="marcius.png", content=content)
        file_name = ""
        gcs.open.assert_called_with(
            file_name, mode='w', content_type="png",
            options={
                'x-goog-acl': 'public-read',
                'cache-control': settings.GOOGLE_CLOUD_STORAGE_DEFAULT_CACHE_CONTROL
            })

        gss_file = mock.Mock()
        gcs.open.return_value = gss_file
        gss_file.write.assert_called_with(content.read())
        content.close.assert_called()
        gss_file.close.assert_called()

    @mock.path("google_handle.storage.google_clound.gcs")
    def test_state_file(self, gcs):
        pass
