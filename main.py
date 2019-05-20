import json
import base64
import logging
from slackclient import SlackClient
from time import time
import os


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

    if _build.get('status') == 'FAILURE':
        send_to_slack(create_slack_message_for_failure(_build), 'Failure')


def create_slack_message_for_failure(data):
    step_failed = ''
    for step in data.get('steps', []):
        if step.get('status') == 'FAILURE':
            step_failed = step.get('id')
            break
    return 'Build id: {} \n Repository: {} \n Step failed: {}'.format(
            data['id'],
            data['source']['repoSource']['repoName'].split('_')[-1],
            step_failed
        )


def send_to_slack(text='Cloud Build!', title='Success'):
    slack_token = os.environ.get("SLACK_TOKEN", "")
    slack_channel = os.environ.get("SLACK_CHANNEL", "_test")
    sc = SlackClient(slack_token)

    sc.api_call(
        "chat.postMessage",
        channel=slack_channel,
        icon_url='https://cloud.google.com/_static/images/cloud/icons/favicons/onecloud/apple-icon.png',
        username='Google Cloud Platform',
        attachments=[{
            'fallback': 'Google Cloud Build Notification Message',
            'color': '#a63636',
            'title': 'Cloud Build Notification',
            'title_link': 'https://api.slack.com/',
            'fields': [{
                'title': title,
                'value': text,
                'short': False
            }],
            'thumb_url': 'https://storage.googleapis.com/public_objects/cloud_build_icon.png',
            'footer': 'google.com:oort-form-dev',
            'ts': time()
            }
        ]
    )
