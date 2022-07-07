import os
import random
import string
import bcrypt, datetime, sys
import hashlib, sys
from mysql.connector import connect, Error
import mysql.connector
from mysql.connector import errorcode
from storage import connect_to_mysql
import logging

MYSQL_HOST = os.environ.get('MYSQL_HOST', '192.168.1.75')
MYSQL_PORT = os.environ.get('MYSQL_PORT', 3307)
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'StageAccount')
MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'secret')

## Connect to MySql
cnx = connect_to_mysql(host=MYSQL_HOST, port=MYSQL_PORT, database=MYSQL_DATABASE, user=MYSQL_USER, password=MYSQL_PASSWORD)

def users(filter, first, max):
    tmp = []
    offset = int(first) * int(max) ## its the page offset [See](https://www.mysqltutorial.org/mysql-limit.aspx)
    select_users_query = "SELECT id_user, user_token, firstname, lastname, email, email as username, verified, active, lang, updated_at, register_Date, remember_token, created_at as birthday, lang as gender FROM {table} LIMIT {offset},{max}".format(table="users", offset=offset, max=max)
    logging.debug(f'{select_users_query}')
    with cnx.cursor() as cursor: 
        cursor.execute(select_users_query)
        columns = cursor.description
        for value in cursor.fetchall():
            dict = {}
            for (index,column) in enumerate(value):
                dict[columns[index][0]] = column            
            tmp.append(dict)
    
    cnx.commit()
    return tmp

def find_by(field, value):
    select_users_query = "SELECT id_user, user_token, firstname, lastname, email, email as username, verified, active, lang, updated_at, register_Date, remember_token, created_at as birthday, lang as gender, password FROM {table} WHERE {field}='{value}' LIMIT 1".format(table="users",field=field, value=value)
    logging.debug(f'{select_users_query}')
    with cnx.cursor() as cursor: 
        cursor.execute(select_users_query)
        columns = cursor.description
        for value in cursor.fetchall():
            dict = {}
            for (index,column) in enumerate(value):
                dict[columns[index][0]] = column
            cnx.commit()         
            return dict


def find_by_with_password(field, value):
    select_users_query = "SELECT id_user, user_token, firstname, lastname, email, email as username, verified, active, lang, updated_at, register_Date, remember_token, created_at as birthday, lang as gender, password FROM {table} WHERE {field}='{value}' LIMIT 1".format(table="users",field=field, value=value)
    logging.debug(f'{select_users_query}')
    with cnx.cursor() as cursor: 
        cursor.execute(select_users_query)
        columns = cursor.description
        for value in cursor.fetchall():
            dict = {}
            for (index,column) in enumerate(value):
                dict[columns[index][0]] = column
            cnx.commit()
            return dict

def insertUser(index, prefix, password):
    index = str(index)
    user_token = index + "_" + prefix + "_user_token"
    firstname = index + "_" + prefix + "_firstname"
    lastname = index + "_" + prefix + "_lastname"
    email = index + "_" + prefix + "@gmail.com"
    password = password
    verified = True
    active = True
    lang = "en"
    updated_at = "2022-07-07 10:10:10"
    created_at = "2022-07-07 10:10:10"
    register_Date = "2022-07-07 10:10:10"
    remember_token = index + "_" + prefix + "_" + "remember_token"
    insert_query = """
        insert into users (user_token, firstname, lastname, email, password, verified, active, lang, updated_at, created_at, register_Date, remember_token) 
        values("{user_token}", "{firstname}", "{lastname}", "{email}", "{password}", "{verified}", "{active}", "{lang}", "{updated_at}", "{created_at}", "{register_Date}", "{remember_token}")
        """.format(user_token=user_token, 
        firstname=firstname, 
        lastname=lastname, 
        email=email, 
        password=password.decode("utf-8"),
        verified=verified, 
        active=active,
        lang=lang,
        updated_at=updated_at,
        created_at=created_at,
        register_Date=register_Date,
        remember_token=remember_token)

    with cnx.cursor() as cursor: 
        cursor.execute(insert_query)
        cnx.commit()

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
   return ''.join(random.choice(chars) for _ in range(size))