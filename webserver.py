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
import simple_http_server.server as server
from storage import find_by, hash_password, password_verify
import os
import logging

HOST = os.environ.get('HOST', '0.0.0.0')
PORT = os.environ.get('PORT', 5000)

# basic logging configuration
logging.basicConfig(format='[%(asctime)s] - %(message)s', level=logging.DEBUG)

# See [HowToMakeControllers](https://github.com/keijack/python-simple-http-server/blob/main/tests/ctrls/my_controllers.py)

# request_map has an alias name `route`, you can select the one you familiar with.
@request_map("/index")
def my_ctrl():
    return {"code": 0, "message": "success"}  # You can return a dictionary, a string or a `simple_http_server.simple_http_server.Response` object.

@request_map("/user_info", method="GET")
def user_info(id=Parameter("id", default="0")):
    # Get the user by id
    user = find_by('id_user', id)
    if not user:
        return 404, Headers({"my-header": "headers"}), {"success": False, "reason": "User not found"}
    return 200, Headers({"my-header": "headers"}), {"success": True, "data": user}

@request_map("/validate", method="POST")
def validate_credentials(json=JSONBody()):
    # Read from the store
    email = json['email']
    password = json['password']

    # check if is a valid tuple (email, password)
    user = find_by('email', email)
    if not user:
        return 404, Headers({"my-header": "headers"}), {"success": False, "reason": "User not found"}

    hashed_password = user["password"]
    logging.debug(f'Plain Password: {password}, Hashed Password: {hashed_password}')
    
    # check if the password match
    hashed = hash_password(password.encode("UTF-8"))
    verify = password_verify(password.encode("UTF-8"), user['password'].encode("UTF-8"))
    if not verify:
        return 401, Headers({"my-header": "headers"}), {"success": False, "reason": "Invalid Password"}

    return 200, Headers({"my-header": "headers"}), {"success": True}

def main(*args):
    # The following method can import several controller files once.
    server.start(host=HOST, port=PORT)

if __name__ == "__main__":
    main()