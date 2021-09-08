from datetime import datetime

from db.connect_db import connect_db


def init_connection():
    server, cnx = connect_db()
    cursor = cnx.cursor()
    return server, cnx, cursor


def create_game(game):
    """
    Create a new game
    """
    server, cnx, cursor = init_connection()
    try:
        game_code = game.get("game_code")
        created_at = datetime.utcnow()

        query = "INSERT INTO games (game_code, created_at) VALUES (%s, %s)"
        value = (game_code, created_at)
        cnx.execute(query, value)
        cnx.commit()
        print("CREATED NEW GAME ", cnx.lastrowid, value)
    except:
        print("FAIL CREATE NEW GAME")

    cursor.close()
    cnx.close()
    server.stop()


def create_state(state):
    """
        Create a new game
        """
    server, cnx, cursor = init_connection()
    try:
        state_str = state.get("state")
        state_code = state.get("state_code")
        game_id = state.get("game_id")
        created_at = datetime.utcnow()

        query = "INSERT INTO states (state, state_code, game_id, created_at) " \
                "VALUES (%s, %s, %i, %s)"
        value = (state_str, state_code, game_id, created_at)
        cnx.execute(query, value)
        print("CREATED NEW COMMENT BATCH ", cnx.lastrowid, value)
    except:
        print("FAIL CREATE NEW GAME")

    cursor.close()
    cnx.close()
    server.stop()


def create_action(action):
    """
        Create a new game
        """
    server, cnx, cursor = init_connection()
    try:
        action_str = action.get("action")
        state_id = action.get("state_id")
        created_at = datetime.utcnow()

        query = "INSERT INTO actions (action, state_id, created_at) VALUES (%s, %i, %s)"
        value = (action_str, state_id, created_at)
        cnx.execute(query, value)
        print("CREATED NEW ACTION ", cnx.lastrowid, value)
    except:
        print("FAIL CREATE NEW GAME")

    cursor.close()
    cnx.close()
    server.stop()


def create_comment(comment):
    """
        Create a new game
        """
    server, cnx, cursor = init_connection()
    try:
        comment = comment.get("comment")
        state_id = comment.get("state_id")
        action_id = comment.get("action_id")
        comment_batches_id = comment.get("comment_batches_id")
        created_at = datetime.utcnow()

        query = "INSERT INTO comments (comment, state_id, action_id, comment_batches_id, created_at) " \
                "VALUES (%s, %i, %i, %i, %s)"
        value = (comment, state_id, action_id, comment_batches_id, created_at)
        cnx.execute(query, value)
        print("CREATED NEW COMMENT ", cnx.lastrowid, value)
    except:
        print("FAIL CREATE NEW GAME")

    cursor.close()
    cnx.close()
    server.stop()


def create_comment_batch(comment_batch):
    """
        Create a new game
        """
    server, cnx, cursor = init_connection()
    try:
        comment = comment_batch.get("comment")
        start_state_id = comment_batch.get("start_state_id")
        end_state_id = comment_batch.get("end_state_id")
        created_at = datetime.utcnow()

        query = "INSERT INTO comment_batches (comment, start_state_id, end_state_id, created_at) " \
                "VALUES (%s, %i, %i, %s)"
        value = (comment, start_state_id, end_state_id, created_at)
        cnx.execute(query, value)
        print("CREATED NEW COMMENT BATCH ", cnx.lastrowid, value)
    except:
        print("FAIL CREATE NEW GAME")

    cursor.close()
    cnx.close()
    server.stop()
