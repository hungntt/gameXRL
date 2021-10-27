from db.api import API


def create_gym_mini_grid():
    api = API(cnx_type='remote', db='pong')
    api.create_gym(gym_code='pong')
    api.close_connection()


if __name__ == '__main__':
    create_gym_mini_grid()
