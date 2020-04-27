# coding:utf-8
from models import database as db

class Team(db.Model):
    __tablename__ = 'team'
    id = db.Column(db.String(255), nullable=False, primary_key=True)
    bot_user_id = db.Column(db.String(255), nullable=False)
    access_token = db.Column(db.String(255), nullable=False)

    def __init__(self, **kwargs):
        super(Team, self).__init__(**kwargs)
