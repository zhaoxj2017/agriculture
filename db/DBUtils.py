import pymysql


def get_instance():
    return pymysql.connect(host="localhost", user="root", passwd="root", db="testdb", use_unicode=True, charset="utf8mb4")


def close(connection):
    if connection is not None:
        connection.close()
