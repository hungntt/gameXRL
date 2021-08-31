from __future__ import print_function

import mysql.connector as sql
from mysql.connector import errorcode
from sshtunnel import SSHTunnelForwarder

DB_NAME = 'xrl'
DB_TABLES = {'games': (
    "CREATE TABLE `games` ("
    " `game_id` int(11) NOT NULL AUTO_INCREMENT,"
    " `game_code` varchar(150) NOT NULL,"
    " `created_at` date NOT NULL,"
    " PRIMARY KEY (`game_id`)"
    ") ENGINE=InnoDB"
), 'states': (
    "CREATE TABLE `states` ("
    " `state_id` int(11) NOT NULL AUTO_INCREMENT,"
    " `game_id` int(11) NOT NULL,"
    " `state` varchar(150) NOT NULL,"
    " `state_code` varchar(150) NOT NULL,"
    " `created_at` date NOT NULL,"
    " PRIMARY KEY (`state_id`), KEY `game_id` (`game_id`),"
    " CONSTRAINT `states_idfk1` FOREIGN KEY (`game_id`) REFERENCES `games` (`game_id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB"
), 'actions': (
    "CREATE TABLE `actions` ("
    " `action_id` int(11) NOT NULL AUTO_INCREMENT,"
    " `state_id` int(11) NOT NULL,"
    " `action` varchar(150) NOT NULL,"
    " `created_at` timestamp NOT NULL,"
    " PRIMARY KEY (`action_id`), KEY `state_id` (`state_id`),"
    " CONSTRAINT `actions_idfk1` FOREIGN KEY (`state_id`) REFERENCES `states` (`state_id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB"
), 'comment_batches': (
    "CREATE TABLE `comment_batches` ("
    " `comment_batches_id` int(11) NOT NULL AUTO_INCREMENT,"
    " `start_state_id` int(11) NOT NULL,"
    " `end_state_id` int(11) NOT NULL,"
    " `comment` varchar(1000) NOT NULL,"
    " `created_at` timestamp NOT NULL,"
    " PRIMARY KEY (`comment_batches_id`)"
    ") ENGINE=InnoDB"
), 'comments': (
    "CREATE TABLE `comments` ("
    " `comment_id` int(11) NOT NULL AUTO_INCREMENT,"
    " `state_id` int(11) NOT NULL,"
    " `action_id` int(11) NOT NULL,"
    " `comment` varchar(1000) NOT NULL,"
    " `comment_batches_id` int(11),"
    " `created_at` timestamp NOT NULL,"
    " PRIMARY KEY (`comment_id`), KEY `state_id` (`state_id`), KEY `action_id` (`action_id`),"
    " CONSTRAINT `comments_idfk1` FOREIGN KEY (`state_id`) REFERENCES `states` (`state_id`) ON DELETE CASCADE,"
    " CONSTRAINT `comments_idfk2` FOREIGN KEY (`action_id`) REFERENCES `actions` (`action_id`) ON DELETE CASCADE,"
    " CONSTRAINT `comments_idfk3` FOREIGN KEY (`comment_batches_id`) "
    " REFERENCES `comment_batches` (`comment_batches_id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB"
)}


### Create MySQL Connection And Connect
def create_database(cursor, cnx):
    try:
        cursor.execute("USE {}".format(DB_NAME))
    except sql.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            try:
                cursor.execute(
                        "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
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
        except sql.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")


def main():
    server = SSHTunnelForwarder(
            ('58.186.80.21', 2056),  # If port 2056 timed out, replace with port 22
            ssh_username="administrator",
            ssh_password="Khang112@",
            remote_bind_address=('0.0.0.0', 1402),
    )
    server.start()
    cnx = sql.connect(
            host="localhost",
            user="root",
            password="password",
            port=server.local_bind_port,
    )
    cursor = cnx.cursor()

    create_database(cursor, cnx)
    create_tables(cursor)

    cursor.close()
    cnx.close()
    server.stop()


if __name__ == '__main__':
    main()
