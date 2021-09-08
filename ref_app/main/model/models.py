from datetime import datetime
from app import db
from app.main.config import ma


class Game(db.Model):
    __tablename__ = 'games'
    game_id = db.Column(db.Integer, primary_key=True)
    game_code = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class GameSchema(ma.ModelSchema):
    pass
