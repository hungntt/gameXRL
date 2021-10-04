from __future__ import print_function

import mysql.connector as sql
from mysql.connector import errorcode

from db.api import API
from db.connect_db import connect_db

DB_NAME = 'minigrid'
DB_TABLES = {'gyms': (
    "CREATE TABLE `gyms` ("
    " `gym_id` int(11) NOT NULL AUTO_INCREMENT,"
    " `gym_code` varchar(150) NOT NULL,"
    " `created_at` datetime NOT NULL,"
    " PRIMARY KEY (`gym_id`)"
    ") ENGINE=InnoDB"
), 'games': (
    "CREATE TABLE `games` ("
    " `game_id` int(11) NOT NULL AUTO_INCREMENT,"
    " `gym_id` int(11) NOT NULL, "
    " `created_at` datetime NOT NULL, "
    " PRIMARY KEY (`game_id`),"
    " CONSTRAINT `games_idfk1` FOREIGN KEY ( `gym_id` ) REFERENCES `gyms` (`gym_id`)"
    ") ENGINE=InnoDB"
), 'observations': (
    "CREATE TABLE `observations` ("
    " `obs_id` int(11) NOT NULL AUTO_INCREMENT,"
    " `gym_id` int(11) NOT NULL,"
    " `game_id` int(11) NOT NULL,"
    " `state` varchar(2000) NOT NULL,"
    " `image` longtext,"
    " `action` int(11) NOT NULL,"
    " `action_meaning` varchar(30),"
    " `done` boolean NOT NULL,"
    " `reward` float(11) NOT NULL,"
    " `comment` longtext,"
    " `comment_batches_id` int(11),"
    " `created_at` datetime NOT NULL,"
    " PRIMARY KEY (`obs_id`), "
    " CONSTRAINT `observations_idfk1` FOREIGN KEY (`gym_id`) REFERENCES `gyms` (`gym_id`), "
    " CONSTRAINT `observations_idfk2` FOREIGN KEY (`game_id`) REFERENCES `games` (`game_id`)"
    ") ENGINE=InnoDB"
), 'comment_batches': (
    "CREATE TABLE `comment_batches` ("
    " `comment_batches_id` int(11) NOT NULL AUTO_INCREMENT,"
    " `start_obs_id` int(11) NOT NULL,"
    " `end_obs_id` int(11) NOT NULL,"
    " `comment` varchar(1000) NOT NULL,"
    " `created_at` datetime NOT NULL,"
    " PRIMARY KEY (`comment_batches_id`), "
    " CONSTRAINT `comment_batches_idfk1` FOREIGN KEY (`start_obs_id`) REFERENCES `observations` (`obs_id`), "
    " CONSTRAINT `comment_batches_idfk2` FOREIGN KEY (`end_obs_id`) REFERENCES `observations` (`obs_id`) "
    ") ENGINE=InnoDB"
)}


### Create MySQL Connection And Connect
def create_database(cursor, cnx):
    try:
        cursor.execute("DROP DATABASE xrl")
        print('Drop old database')
    except sql.errors.DatabaseError:
        print('Database not created yet')
    try:
        cursor.execute("USE {}".format(DB_NAME))
    except sql.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            try:
                cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
            except sql.Error as err:
                print("Failed creating database: {}".format(err))
                exit(1)
            print("Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)


def create_tables(cursor):
    for table_name in DB_TABLES:
        table_description = DB_TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
            cursor.execute("ALTER TABLE {} AUTO_INCREMENT = 1".format(table_name))
        except sql.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")


def create_pre_data(api):
    api.create_gym(gym_code='minigrid')


def main():
    mode = 'server'
    if mode == 'server':
        server, cnx = connect_db('server')
        cursor = cnx.cursor()

        create_database(cursor, cnx)
        create_tables(cursor)

        # api = API(server, cnx, cursor)
        # create_pre_data(api)

        cursor.close()
        cnx.close()
        server.stop()
    elif mode == 'local':
        server, cnx = connect_db('local')
        cursor = cnx.cursor()

        create_database(cursor, cnx)
        create_tables(cursor)

        # api = API(server, cnx, cursor)
        # create_pre_data(api)

        cursor.close()
        cnx.close()


if __name__ == '__main__':
    main()
