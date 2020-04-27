# coding:utf-8
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flask import Flask
from slackeventsapi import SlackEventAdapter
from settings import HOST, PORT, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, SLACK_SIGNING_SECRET, CHATBOT_ENDPOINT, CHATBOT_SECRET_KEY
from models import database as db
from modules import authorize, handle_message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
# Create a dictionary to represent a database to store our token
db.init_app(app)
db.create_all(app=app)

# Route for Oauth flow to redirect to after user accepts scopes
app.route('/authorize', methods=['GET', 'POST'])(authorize)

# Bind the Events API route to your existing Flask app by passing the server
# instance as the last param, or with `server=app`.
slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, '/slack/events', app)
slack_events_adapter.on('message')(handle_message)

if __name__ == '__main__':
    print('start application')
    app.run(host=HOST, port=PORT, debug=True)
