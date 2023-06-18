# import jwt


# 生成 JWT
def generate_jwt(payload=None, secret_key=None):
    token = ""
    # jwt.encode(payload=payload, key=secret_key, algorithm='HS256')
    return token


# 解析 JWT
def parse_jwt(token=None, secret_key=None):
    # try:
    payload = ""
    # jwt.decode(jwt=token, key=secret_key, algorithms=['HS256'])
    return payload
    # except jwt.DecodeError:
    #     # JWT 解码错误
    #     return None
    # except jwt.ExpiredSignatureError:
    #     # JWT 过期错误
    #     return None
