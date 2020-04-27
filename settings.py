# coding:utf-8
from os import environ

# Application setting
PORT = 3000
HOST = '0.0.0.0'

# SQLAlchemy setting
SQLALCHEMY_DATABASE_URI = 'sqlite:///sample.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True


# Slack Bot Application setting
SLACK_CLIENT_ID = environ['SLACK_CLIENT_ID']
SLACK_CLIENT_SECRET = environ['SLACK_CLIENT_SECRET']
SLACK_SIGNING_SECRET = environ['SLACK_SIGNING_SECRET']

# Chatbot setting
# endpoint of Naver Cloud Platform Chatbot
CHATBOT_ENDPOINT = environ['CHATBOT_ENDPOINT']
# secret key of Naver Cloud Platform Chatbot
CHATBOT_SECRET_KEY = environ['CHATBOT_SECRET_KEY']
