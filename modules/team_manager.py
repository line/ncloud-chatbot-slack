# coding:utf-8
from models import database as db
from models import Team

def get_team(team_id):
    team = Team.query.filter(Team.id == team_id).first()
    return team

def upsert_team(team_id, bot_user_id, access_token):
    team = get_team(team_id)
    if team is None:
        # insert
        team = Team(id=team_id, bot_user_id=bot_user_id, access_token=access_token)
        session = db.session()
        session.add(team)
        session.commit()
    else:
        # update
        session = db.session()
        team.bot_user_id = bot_user_id
        team.access_token = access_token
        session.commit()
    return team
