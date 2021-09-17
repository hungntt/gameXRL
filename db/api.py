from datetime import datetime
from db.connect_db import connect_db


class API:
    def __init__(self, server=None, cnx=None, cursor=None):
        if server is None or cnx is None or cursor is None:
            self.server, self.cnx, self.cursor = self.init_connection()
        else:
            self.server, self.cnx, self.cursor = server, cnx, cursor
        self.utc_now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        self.gym_last_id, self.game_last_id, self.comment_batch_last_id = None, None, None

    @staticmethod
    def init_connection():
        server, cnx = connect_db(mode='insert_server')
        cursor = cnx.cursor()
        return server, cnx, cursor

    def close_connection(self):
        """
        Must use it at the end of the program to close the connection if do not pass server from outside
        """
        self.cnx.close()
        self.cursor.close()
        if self.server is not None:
            self.server.close()

    def create_gym(self, gym):
        """
        Create a new gym
        """
        try:
            gym_code = gym.get('gym_code')
            created_at = self.utc_now

            query = "INSERT INTO gyms (gym_code, created_at) VALUES (%s, %s)"
            value = (gym_code, created_at)
            self.cursor.execute(query, value)
            self.cnx.commit()
            print('CREATED NEW GYM ', self.cursor.lastrowid, value)
            self.gym_last_id = self.cursor.lastrowid
        except Exception as e:
            print(e)
            print('FAIL CREATE NEW GYM')

    def create_game(self, game):
        """
        Create a new gym
        """
        try:
            gym_id = game.get("gym_id")
            created_at = self.utc_now

            query = "INSERT INTO games (gym_id, created_at) VALUES (%s, %s)"
            value = (gym_id, created_at)
            self.cursor.execute(query, value)
            self.cnx.commit()
            print("CREATED NEW GAME ", self.cursor.lastrowid, value)
            self.game_last_id = self.cursor.lastrowid
        except Exception as e:
            print(e)
            print("FAIL CREATE NEW GAME")

    def create_observation(self, observation):
        """
        Create a new observation
        """
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
                if 'comment_batches_id' in observation.keys() else -1
            created_at = self.utc_now

            query = "INSERT INTO " \
                    "observations (gym_id, game_id, state, image, comment, " \
                    "action, done, reward, comment_batches_id, created_at) " \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            value = (gym_id, game_id, state, image, comment, action, done, reward, comment_batches_id, created_at)
            self.cursor.execute(query, value)
            self.cnx.commit()
            print('CREATED NEW OBSERVATION  ', self.cursor.lastrowid, value)
        except Exception as e:
            print(e)
            print('FAIL CREATE NEW OBSERVATION')

    def create_comment_batch(self, comment_batch):
        """
        Create a new comment_batch
        """
        try:
            comment = comment_batch.get('comment')
            start_obs_id = comment_batch.get('start_obs_id')
            end_obs_id = comment_batch.get('end_obs_id')
            created_at = self.utc_now

            query = "INSERT INTO comment_batches (comment, start_obs_id, end_obs_id, created_at) " \
                    "VALUES (%s, %s, %s, %s)"
            value = (comment, start_obs_id, end_obs_id, created_at)
            self.cursor.execute(query, value)
            self.cnx.commit()
            print("CREATED NEW COMMENT BATCH ", self.cursor.lastrowid, value)
            self.comment_batch_last_id = self.cursor.lastrowid
        except Exception as e:
            print(e)
            print("FAIL CREATE NEW COMMENT BATCH")

    def select_observations_from_a_game(self, game_id):
        """
        Select a game from game_id
        """
        try:
            query = "SELECT * FROM observations WHERE game_id = %s"
            value = (game_id,)
            self.cursor.execute(query, value)
            observations = self.cursor.fetchall()
            print("Get observations from game_id ", self.cursor.lastrowid, value)
            return observations
        except Exception as e:
            print(e)
            print("Fail to get observations")

    def select_an_observation_from_an_obs_id(self, obs_id):
        """
        Select an observation from an obs_id
        """
        try:
            query = "SELECT * FROM observations WHERE obs_id = %s"
            value = (obs_id,)
            self.cursor.execute(query, value)
            observation = self.cursor.fetchall()
            print("Get an observations from obs_id ", self.cursor.lastrowid, value)
            return observation
        except Exception as e:
            print(e)
            print("Fail to get an observation from obs_id", obs_id)

    def select_observations_from_a_game_from_id_to_id(self, game_id, fobs_id, tobs_id):
        """
        Select a game from game_id, in range obs_id to obs_id
        """
        try:
            query = "SELECT * FROM observations WHERE game_id = %s AND obs_id BETWEEN %s AND %s"
            value = (game_id, fobs_id, tobs_id)
            self.cursor.execute(query, value)
            observations = self.cursor.fetchall()
            print("Get observations from game_id ", self.cursor.lastrowid, value)
            return observations
        except Exception as e:
            print(e)
            print("Fail to get observations")

    def comment_to_an_obs_id(self, obs_id, input_comment):
        """
        Comment to a obs_id state
        """
        try:
            query = "UPDATE observations SET comment = %s WHERE obs_id = %s"
            value = (input_comment, obs_id)
            self.cursor.execute(query, value)
            self.cnx.commit()
            print("Insert comment to obs_id", obs_id, input_comment)
        except Exception as e:
            print(e)
            print("Fail to insert comment ")

    def get_all_games_id_of_a_gym(self, gym_id):
        """
        Get all games id when input a gym id
        """
        try:
            query = "SELECT game_id FROM games WHERE gym_id = %s"
            value = (gym_id,)
            self.cursor.execute(query, value)
            game_ids = self.cursor.fetchall()
            print("Get all game_ids ", self.cursor.lastrowid, value)
            return game_ids
        except Exception as e:
            print(e)
            print("Fail to get observations")

