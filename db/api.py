from datetime import datetime
from db.connect_db import connect_db


def init_connection():
    server, cnx = connect_db(mode='insert_server')
    cursor = cnx.cursor()
    return server, cnx, cursor


def create_gym(gym):
    """
    Create a new gym
    """
    server, cnx, cursor = init_connection()
    try:
        gym_code = gym.get('gym_code')
        created_at = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        query = "INSERT INTO gyms (gym_code, created_at) VALUES (%s, %s)"
        value = (gym_code, created_at)
        cursor.execute(query, value)
        cnx.commit()
        print('CREATED NEW GYM ', cursor.lastrowid, value)
    except Exception as e:
        print(e)
        print('FAIL CREATE NEW GYM')

    cursor.close()
    cnx.close()
    try:
        server.stop()
    except:
        print('Connect to Local Database')


def create_game(game):
    """
    Create a new gym
    """
    server, cnx, cursor = init_connection()
    try:
        gym_id = game.get("gym_id")
        created_at = datetime.utcnow()

        query = "INSERT INTO games (gym_id, created_at) VALUES (%s, %s)"
        value = (gym_id, created_at)
        cursor.execute(query, value)
        cnx.commit()
        print("CREATED NEW GAME ", cursor.lastrowid, value)
    except Exception as e:
        print(e)
        print("FAIL CREATE NEW GAME")

    cursor.close()
    cnx.close()
    try:
        server.stop()
    except:
        print('Connect to Local Database')


def create_observation(observation):
    """
    Create a new observation
    """
    server, cnx, cursor = init_connection()
    try:
        gym_id = observation.get('gym_id')
        game_id = observation.get('game_id')
        state = observation.get('state')
        action = observation.get('action')
        image = observation.get('image')
        done = observation.get('done')
        reward = observation.get('reward')
        comment = observation.get('comment') if 'comment' in observation.keys() else 'None'
        comment_batches_id = observation.get('comment_batches_id') \
            if 'comment_batches_id' in observation.key() else 'None'
        created_at = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        query = "INSERT INTO " \
                "observations (gym_id, game_id, state, image, comment, " \
                "action, done, reward, comment_batches_id, created_at) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        value = (gym_id, game_id, state, image, comment, action, done, reward, comment_batches_id, created_at)
        cursor.execute(query, value)
        cnx.commit()
        print('CREATED NEW OBSERVATION  ', cursor.lastrowid, value)
    except Exception as e:
        print(e)
        print('FAIL CREATE NEW OBSERVATION')

    cursor.close()
    cnx.close()
    try:
        server.stop()
    except:
        print('Connect to Local Database')


def create_comment_batch(comment_batch):
    """
    Create a new comment_batch
    """
    server, cnx, cursor = init_connection()
    try:
        comment = comment_batch.get('comment')
        start_obs_id = comment_batch.get('start_obs_id')
        end_obs_id = comment_batch.get('end_obs_id')
        created_at = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        query = "INSERT INTO comment_batches (comment, start_obs_id, end_obs_id, created_at) " \
                "VALUES (%s, %s, %s, %s)"
        value = (comment, start_obs_id, end_obs_id, created_at)
        cursor.execute(query, value)
        cnx.commit()
        print("CREATED NEW COMMENT BATCH ", cursor.lastrowid, value)
    except Exception as e:
        print(e)
        print("FAIL CREATE NEW COMMENT BATCH")

    cursor.close()
    cnx.close()
    try:
        server.stop()
    except:
        print('Connect to Local Database')


def select_observations_from_a_game(game_id):
    """
    Select a game from game_id
    """
    server, cnx, cursor = init_connection()
    try:
        query = "SELECT * FROM observations WHERE game_id = %s"
        value = game_id
        cursor.execute(query, value)
        print("Get observations from game_id ", cursor.lastrowid, value)
    except Exception as e:
        print(e)
        print("Fail to get observations")

    cursor.close()
    cnx.close()
    try:
        server.stop()
    except:
        print('Connect to Local Database')
