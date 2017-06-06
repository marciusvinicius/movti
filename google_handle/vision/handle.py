# -*- coding: utf-8 -*-

from google.cloud import vision


def get_content(instance):
    vision_client = vision.Client()
    image = vision_client.image(
        content=instance.uplod_to.seq_file.file)
    labels = image.detect_labels()
    content = "".join(x.description for x in labels)
    return content