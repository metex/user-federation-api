import os
import bcrypt, datetime, sys
import hashlib, sys
from mysql.connector import connect, Error
import mysql.connector
from mysql.connector import errorcode
from storage import connect_to_mysql

HOST = os.environ.get('MYSQL_HOST', '192.168.1.75')
PORT = os.environ.get('MYSQL_PORT', 3307)

## Connect to MySql
cnx = connect_to_mysql(host=HOST, port=PORT)

def users(filter, first, max):
    tmp = []
    offset = int(first) * int(max)
    select_users_query = "SELECT * FROM {table} LIMIT {offset},{max}".format(table="users", offset=offset, max=max)
    with cnx.cursor() as cursor: 
        cursor.execute(select_users_query)
        columns = cursor.description
        for value in cursor.fetchall():
            dict = {}
            for (index,column) in enumerate(value):
                dict[columns[index][0]] = column            
            tmp.append(dict)

    return tmp

def find_by(field, value):
    select_users_query = "SELECT * FROM {table} WHERE {field}=\"{value}\"".format(table="users", field=field, value=value)
    with cnx.cursor() as cursor: 
        cursor.execute(select_users_query)
        columns = cursor.description
        for value in cursor.fetchall():
            dict = {}
            for (index,column) in enumerate(value):
                dict[columns[index][0]] = column            
            return dict