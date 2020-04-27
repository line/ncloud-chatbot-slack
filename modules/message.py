# coding:utf-8
import time
import json
import base64
import re
import hmac
import hashlib
import requests
import slack
from settings import CHATBOT_ENDPOINT, CHATBOT_SECRET_KEY
from modules import team_manager

def handle_message(event_data):
    team = team_manager.get_team(event_data['team_id'])

    # In case the app doesn't have access to the oAuth Token
    if team is None:
        print('ERROR: Autenticate the App!')
        return

    message = event_data['event']
    if message.get('subtype') is not None:
        return
    user_id = message['user']
    # If bot reacted own self.
    if user_id == team.bot_user_id:
        return

    # remove mention
    text = re.sub('<@[^>]+>', '', message['text'])
    # request chatbot
    chatbot_response = _request_chatbot(team.id, user_id, text)
    # response to user
    _send_message_each_format(team.access_token, message['channel'], user_id, chatbot_response)
    return


def _send_message_each_format(access_token, channel, user_id, chatbot_response):
    client = slack.WebClient(token=access_token)

    bubbles = chatbot_response['bubbles']
    # send message that formatted for slack to user.
    for bbl in bubbles:
        if bbl['type'] == 'text' and 'quickButtons' in chatbot_response.keys():
            # Form (Quick reply)
            pass
        elif bbl['type'] == 'template':
            # Form (Multiple choice button)
            # Multilink
            # image
            pass
        elif bbl['type'] == 'carousel':
            # image + text
            for card in bbl['data']['cards']:
                # _send_message_each_format(access_token, channel, user_id, chatbot_response)
                cover = card['data']['cover']
                for content in card['data']['contentTable']:
                    pass
        else:
            # default
            content = bbl['data']['description']
            message = '<@%s> %s' % (user_id, content)
            client.chat_postMessage(channel=channel, text=message)


def _request_chatbot(team_id, user_id, text):
    userId = '{team_id},{user_id}'.format(team_id=team_id, user_id=user_id)

    request_body = {
        'version': 'v2',
        'userId': userId,
        'timestamp': _get_timestamp(),
        'bubbles': [{
            'type': 'text',
            'data': {'description': text}
        }],
        'event': 'send'
    }
    ## Request body
    encode_request_body = json.dumps(request_body).encode('UTF-8')
    ## make signature
    signature = _make_signature(CHATBOT_SECRET_KEY, encode_request_body)
    ## headers
    custom_headers = {
        'Content-Type': 'application/json;UTF-8',
        'X-NCP-CHATBOT_SIGNATURE': signature
    }
    chatbot_response = requests.post(headers=custom_headers, url=CHATBOT_ENDPOINT, data=json.dumps(request_body))
    return chatbot_response.json()

def _get_timestamp():
    timestamp = int(time.time() * 1000)
    return timestamp

def _make_signature(secret_key, request_body):
    secret_key_bytes = bytes(secret_key, 'UTF-8')
    signing_key = base64.b64encode(hmac.new(secret_key_bytes, request_body, digestmod=hashlib.sha256).digest())
    return signing_key
