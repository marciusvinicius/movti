# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import mock
from django.test import TestCase
from google_handle.vision.handle import get_content, CREDENTIALS_SCOPED, API_DISCOVERY_FILE


class GoogleVisionTestCase(TestCase):


    @mock.patch("google_handle.vision.handle.httplib2")
    @mock.patch("google_handle.vision.handle.base64")
    @mock.patch("google_handle.vision.handle.GoogleCredentials")
    @mock.patch("google_handle.vision.handle.build")
    def test_get_content(self, build, GoogleCredentials, base64, httplib2):
        instance = mock.Mock()
        instance.upload.read.return_value = "JUST A CONTENT"
        credentials = mock.Mock()
        GoogleCredentials.get_application_default.return_value.create_scoped.return_value = credentials
        service = mock.Mock()
        build.return_value = service

        service_request = mock.Mock()


        service.images.return_value.annotate.return_value = service_request

        response = {
            "responses": [
                {
                    "textAnnotations": [
                        {
                            "description": "Programmer LiFe"
                        },
                        {
                            "description": "Programmer"
                        },
                        {
                            "description": "Life"
                        }
                    ]
                }
            ]
        }

        service_request.execute.return_value = response

        content = get_content(instance)

        GoogleCredentials.get_application_default().create_scoped.assert_called_with(
            CREDENTIALS_SCOPED
        )

        credentials.authorize.assert_called_with(httplib2.Http())

        build.assert_called_with('vision', 'v1',
                                 httplib2.Http(),
                                 discoveryServiceUrl=API_DISCOVERY_FILE)


        service.images().annotate.assert_called_with(
            body={
                'requests': [{
                    'image': {
                        #TODO: Change to use URI from CLOUD
                        'content': base64.b64encode(instance.upload.read()).decode('UTF-8')
                    },
                    'features': [
                        {
                            'type': 'TEXT_DETECTION',

                        },
                        {
                            'type': 'LABEL_DETECTION'
                        }
                    ]
                }]
            }
        )

        self.assertEqual(content, "Programmer LiFe Programmer Life")
