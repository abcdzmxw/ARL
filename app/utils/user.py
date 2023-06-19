import datetime
from flask import g
from flask import request
from app.config import Config
from . import gen_md5, random_choices, get_logger
from .conn import conn_db
import jwt
import pytz

from ..services.system.menu_service import pool

salt = 'arlsalt!@#'
timezone = pytz.timezone('Asia/Shanghai')
logger = get_logger()


def user_login(username=None, password=None):
    if not username or not password:
        return

    query = {"username": username, "password": gen_md5(salt + password)}
    conn = pool.connection()

    # 创建游标对象
    cursor = conn.cursor()

    # 执行查询语句
    query = "SELECT count(*) FROM t_user u WHERE u.username=%s  AND u.password=%s "
    logger.info("query={}".format(query))
    values = (username, gen_md5(salt + password))
    query_total = cursor.execute(query, values)
    logger.info("query_total={}".format(query_total))

    if query_total > 0:
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

        token = gen_md5(random_choices(50))
        payload['token'] = token

        try:
            jwt_token = jwt.encode(payload=payload, key=secret_key, algorithm='HS256')
        except Exception as e:
            logger.info(str(e))

        logger.info("jwt_token= {}, token={}".format(jwt_token, token))
        item = {
            "username": username,
            "jwt_token": jwt_token,
            "token": jwt_token,
            "type": "login"
        }
        conn_db('user').update_one(query, {"$set": {"token": item["token"]}})

        return item


def user_login_header():
    token = request.headers.get("Token") or request.args.get("token")
    jwt_token = request.headers.get("jwt_token") or request.args.get("jwt_token")

    # 这里进行jwt_token校验 TODO

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
        token = request.headers.get("Token") or request.args.get("token")
        logger.info("auth wrapper token1={}".format(token))
        if Config.AUTH and not user_login_header():
            return ret
        logger.info("auth wrapper token2={}".format(token))
        secret_key = Config.JWT_SECRET_KEY
        try:
            decoded_payload = jwt.decode(jwt=token, key=secret_key, algorithms=['HS256'])
            logger.info("auth wrapper decoded_payload={}".format(decoded_payload))
        except jwt.DecodeError:
            # JWT 解码错误
            return ret
        except jwt.ExpiredSignatureError:
            # JWT 过期错误
            return ret

        # 登录成功，将当前登录账户存储到 g 中
        g.current_user = decoded_payload['username']

        return func(*args, **kwargs)

    return wrapper
