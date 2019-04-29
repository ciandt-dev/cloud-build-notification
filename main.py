import json
import base64
import logging
from slackclient import SlackClient
from time import time

def cloud_build_notification(data, context):
    """Background Cloud Function to be triggered by Pub/Sub.
    Args:
         data (dict): The dictionary with data specific to this type of event.
         context (google.cloud.functions.Context): The Cloud Functions event
         metadata.
    """

    _build = dict()
    
    if 'data' in data:
        _build = json.loads(base64.b64decode(data['data']).decode('utf-8'))

    if _build:
        if _build['status'] == 'FAILURE':
            send_to_slack(_build['statusDetail'])
        if _build['status'] == 'WORKING':
            send_to_slack('Working ...')
        if _build['status'] == 'SUCCESS':
            send_to_slack('Success ...')
    
    print(_build)

def send_to_slack(text='Cloud Build!'):
    slack_token = '<slack_token>'
    sc = SlackClient(slack_token)

    sc.api_call(
        "chat.postMessage",
        channel="_test",
        icon_url='https://cloud.google.com/_static/images/cloud/icons/favicons/onecloud/apple-icon.png',
        username='Google Cloud Plattaform',
        attachments=[{
            'fallback': 'Google Cloud Build Notification Message',
            'color': '#36a64f',
            'title': 'Cloud Build Notification',
            'title_link': 'https://api.slack.com/',
            'fields': [{
                'title': 'Success',
                'value': text,
                'short': False
            }],
            'thumb_url': 'https://storage.googleapis.com/public_objects/cloud_build_icon.png',
            'footer': 'gweb-gfw-oort-dev',
            'ts': time()
            }
        ]
    )
