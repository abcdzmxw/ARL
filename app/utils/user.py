from flask import request
from app.config import Config
from . import gen_md5, random_choices, get_logger
from .conn import conn_db
from app.services.system.jwt_service import generate_jwt

salt = 'arlsalt!@#'

logger = get_logger()


def user_login(username=None, password=None):
    if not username or not password:
        return

    query = {"username": username, "password": gen_md5(salt + password)}

    if conn_db('user').find_one(query):

        secret_key = Config.JWT_SECRET_KEY
        token = gen_md5(random_choices(50))

        payload = {'username': username, 'token': token}
        try:
            jwt_token = generate_jwt(payload=payload, secret_key=secret_key)
        except Exception as e:
            logger.info(str(e))

        logger.info("jwt_token= {}".format(jwt_token))
        item = {
            "username": username,
            "jwt_token": jwt_token,
            "token": token,
            "type": "login"
        }
        conn_db('user').update_one(query, {"$set": {"token": item["token"]}})

        return item


def user_login_header():
    token = request.headers.get("Token") or request.args.get("token")

    if not Config.AUTH:
        return True

    item = {
        "username": "ARL-API",
        "token": Config.API_KEY,
        "type": "api"
    }

    if not token:
        return False

    if token == Config.API_KEY:
        return item

    data = conn_db('user').find_one({"token": token})
    if data:
        item["username"] = data.get("username")
        item["token"] = token
        item["type"] = "login"
        return item

    return False


def user_logout(token):
    if user_login_header():
        conn_db('user').update_one({"token": token}, {"$set": {"token": None}})


def change_pass(token, old_password, new_password):
    query = {"token": token, "password": gen_md5(salt + old_password)}
    data = conn_db('user').find_one(query)
    if data:
        conn_db('user').update_one({"token": token}, {"$set": {"password": gen_md5(salt + new_password)}})
        return True
    else:
        return False


import functools


def auth(func):
    ret = {
        "message": "not login",
        "code": 401,
        "data": {}
    }

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if Config.AUTH and not user_login_header():
            return ret

        return func(*args, **kwargs)

    return wrapper
