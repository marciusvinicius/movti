# -*- coding: utf-8 -*-

import base64
from django.core.files.base import ContentFile

from oauth2client.client import GoogleCredentials
from googleapiclient.discovery import build


import httplib2

#TODO: Move this for constant file

API_DISCOVERY_FILE = 'https://vision.googleapis.com/$discovery/rest?version=v1'
CREDENTIALS_SCOPED = ['https://www.googleapis.com/auth/cloud-platform']

def get_content(instance):
    http = httplib2.Http()
    credentials = GoogleCredentials.get_application_default().create_scoped(
        CREDENTIALS_SCOPED)
    credentials.authorize(http)
    service = build('vision', 'v1', http, discoveryServiceUrl=API_DISCOVERY_FILE)

    service_request = service.images().annotate(
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
        })

    response = service_request.execute()
    content = []
    detection_type = None

    for results in response['responses']:
        if 'textAnnotations' in results:
            detection_type = 'textAnnotations'
        elif 'labelAnnotations' in results:
            detection_type = 'labelAnnotations'
        if detection_type:
            for annotations in results[detection_type]:
                content.append(annotations['description'])
    return " ".join(content)


#TODO: USING THE VISION CLIENT

#def get_content(instance):
#    vision_client = vision.Client()
#    image = vision_client.image(
#        content=instance.uplod_to.seq_file.file)
#    labels = image.detect_labels()
#    content = "".join(x.description for x in labels)
#    return content