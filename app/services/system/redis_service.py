import threading

import redis
from redis import ConnectionPool

from app.utils import get_logger

logger = get_logger()


class RedisUtils:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        logger.info("新建RedisUtils................")
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    logger.info("新建实例................")
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host='localhost', port=6379, password=None, db=0, max_connections=10):
        logger.info("RedisUtils初始化----host:{},port={},password={}".format(host, port, password))
        logger.info("_instance={}".format(self._instance))

        self.host = host
        self.port = port
        self.password = password
        self.db = db
        self.max_connections = max_connections
        self.connection_pool = None

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
        decoded_value = value.decode('utf-8')
        logger.info("redis获取值,key={}, value={}".format(key, decoded_value))
        return decoded_value

    def delete(self, key):
        conn = self.get_connection()
        conn.delete(key)


# 创建全局的 RedisUtils 实例
redis_utils = RedisUtils(host='154.39.246.13', port=6379, password='HRwOi8vcy5uYS1j', db=0)
