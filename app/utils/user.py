import datetime

from flask import request
from app.config import Config
from . import gen_md5, random_choices, get_logger
from .conn import conn_db
import jwt
import pytz

salt = 'arlsalt!@#'
timezone = pytz.timezone('Asia/Shanghai')
logger = get_logger()


def user_login(username=None, password=None):
    if not username or not password:
        return

    query = {"username": username, "password": gen_md5(salt + password)}

    if conn_db('user').find_one(query):
        logger.info("username= {}".format(username))
        payload = {'username': username}
        secret_key = Config.JWT_SECRET_KEY
        logger.info("secret_key= {}".format(secret_key))
        # 设置过期时间

        # 获取当前时间，使用指定时区
        current_time = datetime.datetime.now(timezone)
        exp = current_time + datetime.timedelta(seconds=86400)
        payload['exp'] = exp
        logger.info("exp= {}".format(exp))
        try:
            jwt_token = jwt.encode(payload=payload, key=secret_key, algorithm='HS256')
        except Exception as e:
            logger.info(str(e))

        token = gen_md5(random_choices(50))

        logger.info("jwt_token= {}, token={}".format(jwt_token, token))
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
    jwt_token = request.headers.get("jwt_token") or request.args.get("jwt_token")

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
