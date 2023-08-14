import jwt
import pytz
import datetime
from app.config import Config
from app.utils import get_logger

timezone = pytz.timezone('Asia/Shanghai')
logger = get_logger()


# 生成 JWT
def generate_jwt(username, user_id):
    payload = {
        'username': username,
        'user_id': user_id
    }

    secret_key = Config.JWT_SECRET_KEY

    # 设置过期时间
    # 获取当前时间，使用指定时区
    current_time = datetime.datetime.now(timezone)
    exp = current_time + datetime.timedelta(seconds=86400)
    payload['exp'] = exp
    logger.info("secret_key={},exp= {}".format(secret_key, exp))
    token = jwt.encode(payload=payload, key=secret_key, algorithm='HS256')
    return token


# 解析 JWT
def parse_jwt(token):
    secret_key = Config.JWT_SECRET_KEY
    logger.info("secret_key={},token= {}".format(secret_key, token))
    payload = jwt.decode(jwt=token, key=secret_key, algorithms=['HS256'])
    return payload

