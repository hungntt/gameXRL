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
        server, cnx = connect_db(mode='insert_local')
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

    def create_comment_batch(self, start_obs_id, end_obs_id, comment):
        """
        Create a new comment_batch
        """
        try:
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

    def select_observations_from_id_to_id(self, fobs_id, tobs_id):
        """
        Select a game from game_id, in range obs_id to obs_id
        """
        try:
            query = "SELECT * FROM observations WHERE obs_id BETWEEN %s AND %s"
            value = (fobs_id, tobs_id)
            self.cursor.execute(query, value)
            observations = self.cursor.fetchall()
            print("Get observations from %s to %s ", fobs_id, tobs_id, value)
            return observations
        except Exception as e:
            print(e)
            print("Fail to get observations")

    def comment_to_an_obs_id(self, obs_id, input_comment):
        """
        Comment to a obs_id state
        """
        query = "UPDATE observations SET comment = %s WHERE obs_id = %s"
        value = (input_comment, obs_id)
        self.cursor.execute(query, value)
        self.cnx.commit()
        print("Insert comment to obs_id", obs_id, input_comment)

    def comment_to_many_obs_id(self, start_obs_id, end_obs_id, input_comment):
        """
        Comment to a batch of observations
        """
        for i in range(int(start_obs_id), int(end_obs_id) + 1):
            comment_query = "UPDATE observations SET comment = %s WHERE obs_id = %s"
            comment_value = (input_comment, i)
            self.cursor.execute(comment_query, comment_value)
            print("Insert comment to obs_id %s", i, input_comment)
        self.cnx.commit()
        self.create_comment_batch(start_obs_id, end_obs_id, input_comment)

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

    def get_lens_observations(self, **kwargs):
        """
        Get the number of observations
        """
        try:
            if 'game_id' in kwargs.keys():
                # By game_id
                game_id = kwargs.get('game_id')
                query = "SELECT COUNT(*) FROM observations WHERE game_id = %s"
                value = (game_id,)
                self.cursor.execute(query, value)
            elif 'gym_id' in kwargs.keys():
                # By gym_id
                gym_id = kwargs.get('gym_id')
                query = "SELECT COUNT(*) FROM observations WHERE gym_id = %s"
                value = (gym_id,)
                self.cursor.execute(query, value)
            else:
                # All observations
                query = "SELECT COUNT(*) FROM observations"
                self.cursor.execute(query)

            lens_observations = self.cursor.fetchone()
            print("Get the number of observations ", self.cursor.lastrowid)
            return lens_observations[0]
        except Exception as e:
            print(e)
            print("Fail to get the number of observations")

    def get_lens_commented_observations(self, **kwargs):
        """
        Get the number of commented observations
        """
        try:
            if 'game_id' in kwargs.keys():
                # By game_id
                game_id = kwargs.get('game_id')
                query = "SELECT COUNT(*) FROM observations WHERE game_id = %s AND comment != 'None'"
                value = (game_id,)
                self.cursor.execute(query, value)
            elif 'gym_id' in kwargs.keys():
                # By gym_id
                gym_id = kwargs.get('gym_id')
                query = "SELECT COUNT(*) FROM observations WHERE gym_id = %s AND comment != 'None'"
                value = (gym_id,)
                self.cursor.execute(query, value)
            else:
                # All observations
                query = "SELECT COUNT(*) FROM observations WHERE comment != 'None'"
                self.cursor.execute(query)

            lens_observations = self.cursor.fetchone()
            print("Get the number of commented observations ", self.cursor.lastrowid)
            return lens_observations[0]
        except Exception as e:
            print(e)
            print("Fail to get the number of commented observations")
