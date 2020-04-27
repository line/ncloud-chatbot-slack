# coding:utf-8
import slack
from flask import request
from settings import SLACK_CLIENT_ID, SLACK_CLIENT_SECRET
from modules import team_manager

def authorize():
    # Retrieve the auth code and state from the request params
    auth_code = request.args.get('code') or request.json.get('code')

    # Token is not required to call the oauth.v2.access method
    client = slack.WebClient()

    oauth_response = client.oauth_v2_access(
        client_id=SLACK_CLIENT_ID,
        client_secret=SLACK_CLIENT_SECRET,
        code=auth_code
    )

    # Save the bot token, bot user ID and teamID to database
    team = team_manager.upsert_team(
        oauth_response['team']['id'],
        oauth_response['bot_user_id'],
        oauth_response['access_token'])

    # Don't forget to let the user know that auth has succeeded!
    return 'Auth complete!'
