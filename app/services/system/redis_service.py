import threading
import redis
from redis import ConnectionPool

from app.utils import get_logger

# 创建锁对象
redis_lock = threading.Lock()

# 创建全局 RedisUtils 对象
redis_utils = None


class RedisUtils:
    _instance_lock = threading.Lock()
    _initialized = False

    def __init__(self, host='localhost', port=6379, password=None, db=0, max_connections=10):
        self.host = host
        self.port = port
        self.password = password
        self.db = db
        self.max_connections = max_connections
        self.connection_pool = None
        self.connect()

    def connect(self):
        self.connection_pool = ConnectionPool(
            host=self.host,
            port=self.port,
            password=self.password,
            db=self.db,
            max_connections=self.max_connections
        )

    def get_connection(self):
        if not self.connection_pool:
            self.connect()
        return redis.Redis(connection_pool=self.connection_pool)

    def set(self, key, value, expiration=None):
        conn = self.get_connection()
        conn.set(key, value, ex=expiration)

    def get(self, key):
        conn = self.get_connection()
        value = conn.get(key)
        decoded_value = value.decode('utf-8') if value else None
        return decoded_value

    def delete(self, key):
        conn = self.get_connection()
        conn.delete(key)

    def is_initialized(self):
        return self._initialized

    @classmethod
    def instance(cls, *args, **kwargs):
        with cls._instance_lock:
            if not hasattr(cls, "_instance") or not cls._instance:
                cls._instance = cls(*args, **kwargs)
        return cls._instance


logger = get_logger()


def get_redis_utils():
    global redis_utils

    if redis_utils is None:
        logger.info("redis_utils is Node")
        with redis_lock:
            logger.info("get_redis_utils 获取锁")
            if redis_utils is None:
                logger.info("get_redis_utils 开始初始化RedisUtils")
                redis_utils = RedisUtils.instance(
                    host='154.39.246.13',
                    port=6379,
                    password='HRwOi8vcy5uYS1j',
                    db=0
                )
                logger.info("get_redis_utils 初始化RedisUtils redis_utils={}".format(redis_utils))
                redis_utils._initialized = True
    return redis_utils
