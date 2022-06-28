import hashlib
import secrets
import bcrypt, datetime, sys
import hashlib, sys

# [Python bcrypt](https://zetcode.com/python/bcrypt/)

def hash_password(secret):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(secret, salt)

def password_verify(password, hash):
    return True if bcrypt.checkpw(password, hash) else False

## Alternative 2 - Greate success
secret = "1234567".encode("utf-8")
hashed = hash_password(secret)
print(hashed)
print(hashed.decode("UTF-8"))
verify = password_verify(secret, hashed)
print(verify)