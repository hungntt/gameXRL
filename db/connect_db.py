from sshtunnel import SSHTunnelForwarder
import mysql.connector as sql


def connect_db(mode='server'):
    server, cnx = None, None
    if mode == 'server':
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
    elif mode == 'local':
        cnx = sql.connect(
                host="localhost",
                user="root",
                password="admin",
                database="xrl"
        )
    elif mode == 'insert_server':
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
                database="xrl",
        )
    elif mode == 'insert_local':
        cnx = sql.connect(
                host="localhost",
                user="root",
                password="Hikari@123",
                database="xrl",
        )
    return server, cnx
