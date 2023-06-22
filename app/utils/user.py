import datetime
from flask import g
from flask import request
from app.config import Config
from . import gen_md5, random_choices, get_logger
import jwt
import pytz
import functools
from ..services.system.db_utils import get_db_utils
from ..services.system.redis_service import get_redis_utils

redis_utils = get_redis_utils()
db_utils = get_db_utils()

salt = 'arlsalt!@#'
timezone = pytz.timezone('Asia/Shanghai')
logger = get_logger()


def user_login(username=None, password=None, validate_code=None, user_key=None):
    if not username or not password or not validate_code or not user_key:
        if not user_key:
            # 删除redis的验证码
            redis_utils.delete(key=user_key)
        return None

    redis_validate_code = redis_utils.get(key=user_key)
    if not redis_validate_code or redis_validate_code != validate_code:
        # 删除redis的验证码
        redis_utils.delete(key=user_key)
        return None

    # 执行查询语句
    query_total_sql = "SELECT count(*) FROM t_user u WHERE u.username=%s  AND u.password=%s "
    values = (username, gen_md5(salt + password))
    query_total = db_utils.get_query_total(sql=query_total_sql, args=values)

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
            "token": jwt_token,
            "type": "login"
        }

        update_sql = "UPDATE t_user SET token = %s WHERE username = %s"
        new_values = (jwt_token, username)
        db_utils.execute_update(sql=update_sql, args=new_values)

        return item
    else:

        # 删除redis的验证码
        redis_utils.delete(key=user_key)
        return None


def user_login_header(token):
    logger.info("user_login_header.........")
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


def user_logout(token):
    if user_login_header(token):
        secret_key = Config.JWT_SECRET_KEY
        payload = jwt.decode(jwt=token, key=secret_key, algorithms=['HS256'])
        update_sql = "UPDATE t_user SET token = null WHERE username = %s AND token=%s"
        new_values = (payload['username'], token)
        logger.info("user_login_header: {},{}".format(payload['username'], token))
        db_utils.execute_update(sql=update_sql, args=new_values)
        # conn_db('user').update_one({"token": token}, {"$set": {"token": None}})


def change_pass(token, old_password, new_password):
    # query = {"token": token, "password": gen_md5(salt + old_password)}
    # data = conn_db('user').find_one(query)
    secret_key = Config.JWT_SECRET_KEY

    try:
        payload = jwt.decode(jwt=token, key=secret_key, algorithms=['HS256'])
    except Exception as e:
        logger.exception(e)
        return None

    logger.info("修改密码payload={}".format(payload))

    username = payload['username']
    # 执行查询语句
    query_sql = "SELECT count(*) FROM t_user u WHERE u.username=%s  AND u.password=%s AND u.token=%s "
    values = (username, gen_md5(salt + old_password), token)
    query_total = db_utils.get_query_total(sql=query_sql, args=values)

    logger.info("query_sql={}, query_total={}".format(query_sql, query_total))

    if query_total > 0:
        # conn_db('user').update_one({"token": token}, {"$set": {"password": gen_md5(salt + new_password)}})
        update_sql = "UPDATE t_user SET password = %s, token=null WHERE username = %s"
        new_values = (gen_md5(salt + new_password), username)
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
        logger.info("auth wrapper token1={}".format(token))

        logger.info("auth wrapper Config.AUTH1={}".format(Config.AUTH))
        if Config.AUTH and not user_login_header(token=token):
            logger.info("auth wrapper Config.AUTH2={}".format(Config.AUTH))
            return ret
        logger.info("auth wrapper token2={}".format(token))
        secret_key = Config.JWT_SECRET_KEY
        try:
            decoded_payload = jwt.decode(jwt=token, key=secret_key, algorithms=['HS256'])
            logger.info("auth wrapper decoded_payload={}".format(decoded_payload))
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
