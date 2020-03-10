# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.conf import settings
from google_handle.storage.handle import GoogleCloudStorage

import mock


class GoogleStorageTestCase(TestCase):

    def setUp(self):
        import sys
        sys.path.insert(1, 'google-cloud-sdk/platform/google_appengine')
        sys.path.insert(1, 'google-cloud-sdk/platform/google_appengine/lib/yaml/lib')
        sys.path.insert(1, '../../../lib')

    def test_create_init(self):
        storage = GoogleCloudStorage()
        self.assertEqual(storage.location, settings.GOOGLE_CLOUD_STORAGE_BUCKET)
        self.assertEqual(storage.base_url, settings.GOOGLE_CLOUD_STORAGE_URL)

    @mock.path("google_handle.storage.handle.ContentFile")
    @mock.path("google_handle.storage.handle.gcs")
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
        ContentFile.assert_called_with(gcs_file.read())

    @mock.path("google_handle.storage.handle.gcs")
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

    @mock.path("google_handle.storage.handle.gcs")
    def test_state_file(self, gcs):
        storage = GoogleCloudStorage()
        storage.stat_file("image")
        filename = "/%s/%s" % (settings.GOOGLE_CLOUD_STORAGE_BUCKET, "image")
        gcs.assert_callet_with(filename)

    @mock.path("google_handle.storage.handle.gcs")
    def test_state_raise(self, gcs):
        storage = GoogleCloudStorage()
        state = storage.stat_file("image")
        gcs.stat.side_effect(Exception())
        self.assertEqual(state, None)
