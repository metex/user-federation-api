import datetime
import json
from simple_http_server import FilterContex, ModelDict, Redirect, RegGroup, RequestBodyReader
from simple_http_server import request_map
from simple_http_server import Response
from simple_http_server import MultipartFile
from simple_http_server import Parameter
from simple_http_server import Parameters
from simple_http_server import Header
from simple_http_server import JSONBody
from simple_http_server import HttpError
from simple_http_server import StaticFile
from simple_http_server import Headers
from simple_http_server import Cookies
from simple_http_server import Cookie
from simple_http_server import Redirect
from simple_http_server import ModelDict
from simple_http_server import request_map, route
from simple_http_server import controller
from simple_http_server import PathValue
from simple_http_server import Parameter
import simple_http_server.server as server
from storage import connect_to_mysql, find_by, hash_password, password_verify
import os
import logging
import repository as repository

HOST = os.environ.get('HOST', '0.0.0.0')
PORT = os.environ.get('PORT', 5000)

# basic logging configuration
logging.basicConfig(format='[%(asctime)s] - %(message)s', level=logging.DEBUG)

# See [HowToMakeControllers](https://github.com/keijack/python-simple-http-server/blob/main/tests/ctrls/my_controllers.py)

def defaultconverter(o):
  if isinstance(o, datetime.datetime):
      return o.__str__()


@request_map("/**")
def wildcard_match(path_val=PathValue(), headers=Headers(), parameters=Parameters(), cookies=Cookies(), body=RequestBodyReader()):
    dict = {}
    dict['path'] = path_val
    dict['headers'] = headers
    dict['parameters'] = parameters
    dict['body'] = body
    logging.debug(dict)
    # logging.debug(f'Path value: {path_val}')
    # logging.debug(f'Headers value: {headers}')
    # logging.debug(f'Parameters value: {parameters}')
    # logging.debug(f'Cookies value: {cookies}')

# request_map has an alias name `route`, you can select the one you familiar with.
@request_map("/index")
def my_ctrl():
    return {"code": 0, "message": "success"}  # You can return a dictionary, a string or a `simple_http_server.simple_http_server.Response` object.

@request_map("/users", method="GET")
def users(filter=Parameter("filter", default=""), first=Parameter("first", default="0"), max=Parameter("max", default="2")):
    result = repository.users(filter, first, max)
    return 200, Headers({"my-header": "headers"}), json.dumps(result, default = defaultconverter)

@request_map("/user/{value}", method="GET")
def user_by(value: PathValue, filter=Parameter("filter", default="id_user")):
     # Get the user by id
    result = repository.find_by(filter, value)
    if not result:
        return 404, Headers({"my-header": "headers"}), {"success": False, "reason": "User not found"}
    return 200, Headers({"my-header": "headers"}), json.dumps(result, default = defaultconverter)

@request_map("/validate", method="POST")
def validate_credentials(json=JSONBody()):
    # Read from the store
    username = json['username'] ## username here is the email in the skoiy users table
    password = json['password']

    # check if is a valid tuple (email, password)
    user = repository.find_by_with_password('email', username)
    if not user:
        return 404, Headers({"my-header": "headers"}), {"verified": False, "reason": "User not found"}

    hashed_password = user["password"]
    logging.debug(f'Plain Password: {password}, Hashed Password: {hashed_password}')

    # check if the password match
    hashed = hash_password(password.encode("UTF-8"))
    verify = password_verify(password.encode("UTF-8"), user['password'].encode("UTF-8"))
    if not verify:
        return 401, Headers({"my-header": "headers"}), {"verified": False, "reason": "Invalid Password"}

    return 200, Headers({"my-header": "headers"}), {"verified": True}

@request_map("/user/{value}/credentials", method="GET")
def user_credentials():
    return 200, Headers({"my-header": "headers"}), {"value": "$2y$10$1/xlmIBAoz1SMgMTyAtr8eKhE33Truhg/t5xjic6VXclhgfEINv4i", "salt": "salt", "algorithm": "bcrypt", "iterations": 27500, "type": "password"}

@request_map("/user_info", method="GET")
def user_info(id=Parameter("id", default="0")):
    # Get the user by id
    user = find_by('id_user', id)
    if not user:
        return 404, Headers({"my-header": "headers"}), {"success": False, "reason": "User not found"}
    return 200, Headers({"my-header": "headers"}), {"success": True, "data": user}

def main(*args):
    # The following method can import several controller files once.
    server.start(host=HOST, port=PORT)

if __name__ == "__main__":
    main()