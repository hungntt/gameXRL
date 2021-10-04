import mysql.connector as sql
from datetime import datetime
from db.connect_db import connect_db


def main():
    server, cnx = connect_db('local')
    cursor = cnx.cursor()

    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    query = "INSERT INTO games (gym_id, created_at) VALUES (%s, %s)"
    value = (1, now)
    try:
        cursor.execute(query, value)
        cnx.commit()
    except sql.Error as err:
        print(err.msg)

    cursor.close()
    cnx.close()


if __name__ == '__main__':
    main()
