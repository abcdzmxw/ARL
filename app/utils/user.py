import datetime
from flask import g
from flask import request
from app.config import Config
from . import gen_md5, random_choices, get_logger
from .conn import conn_db
import jwt
import pytz
from app import utils
import pymysql
from dbutils.pooled_db import PooledDB

pool = PooledDB(
    creator=pymysql,  # 使用pymysql作为连接器
    host='192.168.1.100',
    user='root',
    password='Hjrtnbec*38',
    database='galaxy_arl',
    maxconnections=10,  # 连接池大小
    autocommit=True,  # 自动提交事务
    charset='utf8'  # 设置字符集
)

salt = 'arlsalt!@#'
timezone = pytz.timezone('Asia/Shanghai')
logger = get_logger()


def user_login(username=None, password=None):
    if not username or not password:
        return

    # query = {"username": username, "password": gen_md5(salt + password)}
    logger.info("username:{},password={}".format(username, password))
    # 创建数据库连接
    conn = pool.connection()

    # 创建游标对象
    cursor = conn.cursor()

    # 执行查询语句
    db_query = "SELECT count(*) FROM t_user u WHERE u.username=%s  AND u.password=%s "
    logger.info("query={}".format(db_query))
    values = (username, gen_md5(salt + password))
    cursor.execute(db_query, values)
    query_total = cursor.fetchone()[0]
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
        # conn_db('user').update_one(query, {"$set": {"token": item["token"]}})
        conn = pool.connection()

        # 创建游标对象
        cursor = conn.cursor()
        update_sql = "UPDATE t_user SET token = %s WHERE username = %s"
        new_values = (jwt_token, username)
        cursor.execute(update_sql, new_values)
        conn.commit()
        # 关闭游标和数据库连接
        cursor.close()
        conn.close()

        return item


def user_login_header():
    token = request.headers.get("Token") or request.args.get("token")
    logger.info("user_login_header1, token: {}", token)
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

    logger.info("user_login_header2, token: {}", token)
    secret_key = Config.JWT_SECRET_KEY
    payload = jwt.decode(jwt=token, key=secret_key, algorithms=['HS256'])
    logger.info("user_login_header3, token: {},payload={}", token, payload)
    # data = conn_db('user').find_one({"token": token})
    if payload:
        item["username"] = payload['username']
        item["token"] = token
        item["type"] = "login"
        return item

    return False


def user_logout(token):
    if user_login_header():
        logger.info("user_logout: 这里不执行 conn_db('user')")
        # conn_db('user').update_one({"token": token}, {"$set": {"token": None}})


def change_pass(token, old_password, new_password):
    # query = {"token": token, "password": gen_md5(salt + old_password)}
    # data = conn_db('user').find_one(query)
    secret_key = Config.JWT_SECRET_KEY
    payload = jwt.decode(jwt=token, key=secret_key, algorithms=['HS256'])

    logger.info("修改密码payload={}".format(payload))
    conn = pool.connection()

    # 创建游标对象
    cursor = conn.cursor()
    username = payload['username']
    # 执行查询语句
    query_sql = "SELECT count(*) FROM t_user u WHERE u.username=%s  AND u.password=%s AND u.token=%s "
    logger.info("query_sql={}".format(query_sql))
    values = (username, gen_md5(salt + old_password), token)
    cursor.execute(query_sql, values)
    query_total = cursor.fetchone()[0]
    logger.info("query_total={}".format(query_total))

    if query_total > 0:
        # conn_db('user').update_one({"token": token}, {"$set": {"password": gen_md5(salt + new_password)}})
        update_sql = "UPDATE t_user SET password = %s, token=null WHERE username = %s"
        new_values = (gen_md5(salt + new_password), username)
        cursor.execute(update_sql, new_values)
        conn.commit()
        # 关闭游标和数据库连接
        cursor.close()
        conn.close()

        return True
    else:
        # 关闭游标和数据库连接
        cursor.close()
        conn.close()
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
        except Exception as e:
            logger.exception(e)
            return ret

        conn = pool.connection()
        cursor = conn.cursor()
        username = decoded_payload['username']
        logger.info("username={},token={}".format(username, token))
        # 执行查询语句
        query_sql = "SELECT count(*) FROM t_user u WHERE u.username=%s  AND u.token=%s "
        logger.info("query_sql={}".format(query_sql))
        values = (username, token)
        cursor.execute(query_sql, values)
        query_total = cursor.fetchone()[0]
        logger.info("query_total={},username={},token={}".format(query_total, username, token))
        if query_total == 0:
            logger.info(
                "进入返回 {}".format(ret))
            return ret

        logger.info("查询不到数据不会执行到这里query_total:{},username={},token={}".format(query_total, username, token))
        # 登录成功，将当前登录账户存储到 g 中
        g.current_user = decoded_payload['username']

        return func(*args, **kwargs)

    return wrapper


def reset_password(user_id, password):
    conn = pool.connection()

    # 创建游标对象
    cursor = conn.cursor()
    # 执行查询语句
    update_sql = "Update t_user set password=%s, token= null Where user_id=%s "

    values = (gen_md5(salt + password), user_id)
    cursor.execute(update_sql, values)

    conn.commit()
    # 关闭游标和数据库连接
    cursor.close()
    conn.close()

