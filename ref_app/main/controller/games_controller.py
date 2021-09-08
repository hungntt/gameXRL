from flask import (make_response, abort, )

from app.main.model.models import Game


def create(game):
    """
    Create a new game
    """
    game_code = game.get("game_code")

    existing_game = (
        Game.query.filter(Game.game_code == game_code).one_or_none()
    )

    if existing_game is None:
        schema = GameSchema()
