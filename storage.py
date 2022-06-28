import bcrypt, datetime, sys
import hashlib, sys

accounts = [
    {'id_account': '1', 'account_token': 'AC_TOKEN1', 'company_name': 'Acme1', 'email': 'ac1@gmail.com', 'verified': True, 'active': True, 'updated_at': '2022-06-09 11:10:22', 'created_at': '2022-06-09 11:10:22'},
    {'id_account': '2', 'account_token': 'AC_TOKEN2', 'company_name': 'Acme2', 'email': 'ac2@gmail.com', 'verified': True, 'active': True, 'updated_at': '2022-06-09 11:10:22', 'created_at': '2022-06-09 11:10:22'},
    {'id_account': '3', 'account_token': 'AC_TOKEN3', 'company_name': 'Acme3', 'email': 'ac3@gmail.com', 'verified': True, 'active': True, 'updated_at': '2022-06-09 11:10:22', 'created_at': '2022-06-09 11:10:22'},
]

users = [
    {'id_user': '1', 'user_token': 'j6BhUMiG2RKP1eVTsqWbl0woT', 'firstname': 'John', 'lastname': "Doe", 'email': 'john1@gmail.com', 'password': '$2y$10$1/xlmIBAoz1SMgMTyAtr8eKhE33Truhg/t5xjic6VXclhgfEINv4i', 'verified': True, 'active': True, 'lang': 'pt', 'updated_at': '2022-06-09 11:10:22', 'created_at': '2022-06-09 11:10:22'},
    {'id_user': '2', 'user_token': 'hCnuiLISUFYzD1e54ea6O54Ox', 'firstname': 'John', 'lastname': "Doe", 'email': 'john2@gmail.com', 'password': '$2y$10$1/xlmIBAoz1SMgMTyAtr8eKhE33Truhg/t5xjic6VXclhgfEINv4i', 'verified': True, 'active': True, 'lang': 'pt', 'updated_at': '2022-06-09 11:10:22', 'created_at': '2022-06-09 11:10:22'},
]

users_accounts = [
    {'id_user': '1', 'id_account': '1', 'id_role': 1, 'last_login': '2022-06-09 11:10:19', 'register_date': '2022-06-09 11:10:19' },
    {'id_user': '1', 'id_account': '2', 'id_role': 1, 'last_login': '2022-06-09 11:10:19', 'register_date': '2022-06-09 11:10:19' },
    {'id_user': '1', 'id_account': '3', 'id_role': 1, 'last_login': '2022-06-09 11:10:19', 'register_date': '2022-06-09 11:10:19' },
]

def find_by(k, v):

    for user in users:
        if user[k] == v:
            return user
        else:
            return False

def hash_password(secret):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(secret, salt)

def password_verify(password, hash):
    return True if bcrypt.checkpw(password, hash) else False
