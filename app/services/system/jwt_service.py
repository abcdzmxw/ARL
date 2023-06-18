from app import utils

logger = utils.get_logger()

# 生成 JWT
def generate_jwt(payload=None, secret_key=None):
    token = ""
    logger.info("进来了generate_jwt")
    return token
