import sys
sys.path.append('/home/silver/gameXRL-master')

import mysql.connector as sql
from mysql.connector import errorcode

from db.api import API
from db.connect_db import connect_db
from datetime import datetime

def main():
    server, cnx = connect_db('local')
    cursor = cnx.cursor()

    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    query = "INSERT INTO gyms (gym_code, created_at) VALUES (%s, %s)"
    value = ("miniGrid", now)
    try:
        cursor.execute(query, value)
        cnx.commit()
    except sql.Error as err:
        print(err.msg)

    cursor.close()
    cnx.close()


if __name__ == '__main__':
    main()