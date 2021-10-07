from sshtunnel import SSHTunnelForwarder
import mysql.connector as sql


def connect_db(cnx_type, db=None):
    server, cnx = None, None
    if db is None:
        if cnx_type == 'remote':
            # Insert directly to the main database by server: only for create/drop/alter databases
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
        elif cnx_type == 'server':
            cnx = sql.connect(
                    host="localhost",
                    user="root",
                    port="1402",
                    password="password",
            )
        elif cnx_type == 'local':
            cnx = sql.connect(
                    host="localhost",
                    user="root",
                    port="3306",
                    password="Hikari@123",
            )
    else:
        if cnx_type == 'remote':
            # Insert directly to the pong database by server
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
                    database=db,
            )
        elif cnx_type == 'server':
            cnx = sql.connect(
                    host="localhost",
                    user="root",
                    port="1402",
                    password="password",
                    database=db,
            )
        elif cnx_type == 'local':
            cnx = sql.connect(
                    host="localhost",
                    user="root",
                    port="3306",
                    password="Hikari@123",
            )
    return server, cnx
