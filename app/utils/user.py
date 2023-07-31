import datetime
from flask import g
from flask import request
from app.config import Config
from . import gen_md5, random_choices, get_logger
import jwt
import pytz
import functools
from ..services.system.db_utils import get_db_utils
from ..services.system.jwt_service import generate_jwt, parse_jwt
from ..services.system.redis_service import get_redis_utils

salt = 'arlsalt!@#'

redis_utils = get_redis_utils()
db_utils = get_db_utils()
logger = get_logger()


def login_log(username, user_id, token):
    insert_sql = "INSERT INTO t_login_log (username, user_id, token) VALUES (%s, %s, %s)"
    values = (username, user_id, token)
    logger.info("login_log, insert_sql={}, values={}".format(insert_sql, values))
    db_utils.execute_insert(sql=insert_sql, args=values)


def user_login2(username=None, password=None, validate_code=None, user_key=None):
    returnObj = {'code': 401}

    # 验证码只能用一次 调用了登录接口后没成功就的重新获取验证码
    if not username or not password or not validate_code or not user_key:
        if not user_key:
            # 删除redis的验证码
            redis_utils.delete(key=user_key)

        returnObj['message'] = '登录信息不能为空!'
        return returnObj

    # 从redis获取校验码进行验证
    redis_validate_code = redis_utils.get(key=user_key)
    if not redis_validate_code or redis_validate_code.lower() != validate_code.lower():
        if redis_validate_code:
            # 删除redis的验证码
            redis_utils.delete(key=user_key)
        returnObj['message'] = '验证码错误!'
        return returnObj

    # 执行查询语句
    query_ql = "SELECT u.user_id,u.name,u.username,u.email,u.phone FROM  t_user u WHERE u.username=%s  AND u.password=%s "
    values = (username, gen_md5(salt + password))
    user_obj = db_utils.get_one(sql=query_ql, args=values)
    if user_obj:
        logger.info("登录查询用户成功,user={}".format(user_obj))
        logger.info("username= {}".format(username))
        jwt_token = generate_jwt(username, user_obj['user_id'])
        logger.info("jwt_token= {}".format(jwt_token))
        login_log(username, user_obj['user_id'], jwt_token)
        update_sql = "UPDATE t_user SET last_login_time=NOW(), token = %s WHERE username = %s "
        new_values = (jwt_token, username)
        db_utils.execute_update(sql=update_sql, args=new_values)
        returnObj['username'] = username
        returnObj['token'] = jwt_token
        returnObj['code'] = 200
        returnObj['message'] = 'success'

        return returnObj
    else:
        # 删除redis的验证码
        redis_utils.delete(key=user_key)
        returnObj['message'] = '用户名密码错误!'
        return returnObj


def user_login(username=None, password=None, validate_code=None, user_key=None):
    returnObj = {'code': 401}

    # 验证码只能用一次 调用了登录接口后没成功就的重新获取验证码
    if not username or not password:
        returnObj['message'] = '登录信息不能为空!'
        return returnObj

    # 执行查询语句
    query_ql = "SELECT u.user_id,u.name,u.username,u.email,u.phone FROM  t_user u WHERE u.username=%s  AND u.password=%s "
    values = (username, gen_md5(salt + password))
    user_obj = db_utils.get_one(sql=query_ql, args=values)
    if user_obj:
        logger.info("登录查询用户成功,user={}".format(user_obj))
        logger.info("username= {}".format(username))
        jwt_token = generate_jwt(username, user_obj['user_id'])
        logger.info("jwt_token= {}".format(jwt_token))
        login_log(username, user_obj['user_id'], jwt_token)
        update_sql = "UPDATE t_user SET last_login_time=NOW(), token = %s WHERE username = %s"
        new_values = (jwt_token, username)
        db_utils.execute_update(sql=update_sql, args=new_values)
        returnObj['username'] = username
        returnObj['token'] = jwt_token
        returnObj['code'] = 200
        returnObj['message'] = 'success'

        return returnObj
    else:
        returnObj['message'] = '用户名密码错误!'
        return returnObj


def user_login_header(token):
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

    try:
        secret_key = Config.JWT_SECRET_KEY
        payload = jwt.decode(jwt=token, key=secret_key, algorithms=['HS256'])
    except Exception as e:
        logger.exception(e)
        return False

    if payload:
        item["username"] = payload['username']
        item["token"] = token
        item["type"] = "login"
        return item

    return False


def user_logout():
    update_sql = "UPDATE t_user SET token = null WHERE username = %s"
    new_values = (g.get('current_user'))
    db_utils.execute_update(sql=update_sql, args=new_values)


def change_pass(token, old_password, new_password):
    current_user = g.get('current_user')
    # 执行查询语句
    query_sql = "SELECT count(*) FROM t_user u WHERE u.username=%s  AND u.password=%s AND u.token=%s "
    values = (current_user, gen_md5(salt + old_password), token)
    query_total = db_utils.get_query_total(sql=query_sql, args=values)

    logger.info("query_sql={}, query_total={}".format(query_sql, query_total))

    if query_total > 0:
        # conn_db('user').update_one({"token": token}, {"$set": {"password": gen_md5(salt + new_password)}})
        update_sql = "UPDATE t_user SET password = %s, token=null WHERE username = %s"
        new_values = (gen_md5(salt + new_password), current_user)
        db_utils.execute_update(sql=update_sql, args=new_values)
        return True
    else:
        return False


def auth(func):
    ret = {
        "message": "not login",
        "code": 401,
        "data": {}
    }

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Token") or request.args.get("token")

        logger.info("auth wrapper Config.AUTH1={}".format(Config.AUTH))
        if Config.AUTH and not user_login_header(token=token):
            logger.info("auth wrapper Config.AUTH2={}".format(Config.AUTH))
            return ret
        logger.info("auth wrapper token2={}".format(token))
        try:
            decoded_payload = parse_jwt(token=token)
        except Exception as e:
            logger.exception(e)
            return ret

        username = decoded_payload['username']
        logger.info("username={},token={}".format(username, token))
        # 执行查询语句
        query_sql = "SELECT count(*) FROM t_user u WHERE u.username=%s  AND u.token=%s "
        values = (username, token)

        logger.info("query_sql={},values={}".format(query_sql, values))

        query_total = db_utils.get_query_total(sql=query_sql, args=values)
        logger.info("query_total={},username={},token={}".format(query_total, username, token))
        if query_total == 0:
            logger.info("进入返回 {}".format(ret))
            return ret

        logger.info(
            "查询不到数据不会执行到这里query_total:{},username={},token={}".format(query_total, username, token))
        # 登录成功，将当前登录账户存储到 g 中
        g.current_user = decoded_payload['username']

        return func(*args, **kwargs)

    return wrapper


def reset_password(user_id, password):
    # 执行查询语句
    update_sql = "Update t_user set password=%s, token= null Where user_id=%s "
    values = (gen_md5(salt + password), user_id)
    db_utils.execute_update(sql=update_sql, args=values)
