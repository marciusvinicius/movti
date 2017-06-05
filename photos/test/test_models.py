# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from photos.models import Photo


class PhotoTestCase(TestCase):
    """
    Testing models
    """

    def test_to_string(self):
        photo = Photo(name="Park St.Amado")
        photo.save()

        self.assertEqual(str(photo), photo.name)


    def test_validation_fields(self):
        photo = Photo(name="")
        with self.assertRaises(IOError):
            photo.save()
