import jwt


# 生成 JWT
def generate_jwt(payload, secret_key):
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token


# 解析 JWT
def parse_jwt(token, secret_key):
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.DecodeError:
        # JWT 解码错误
        return None
    except jwt.ExpiredSignatureError:
        # JWT 过期错误
        return None
