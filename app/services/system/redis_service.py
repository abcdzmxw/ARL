import threading

import redis
from redis import ConnectionPool
from app.utils import get_logger

logger = get_logger()

_instance = None
_lock = threading.Lock()


def get_redis_utils():
    global _instance
    if _instance is None:
        logger.info("Instance does not exist, acquiring lock...")
        with _lock:
            logger.info("Instance does not exist, lock acquired...")
            if _instance is None:
                logger.info("Creating RedisUtils instance...")
                _instance = RedisUtils(
                    host='154.39.246.13',
                    port=6379,
                    password='HRwOi8vcy5uYS1j',
                    db=0
                )
    return _instance


class RedisUtils:
    def __init__(self, host='localhost', port=6379, password=None, db=0, max_connections=10):
        logger.info("RedisUtils initialized ---- host:{}, port={}, password={}".format(host, port, password))
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
        decoded_value = value.decode('utf-8')
        logger.info("RedisUtils: get value, key={}, value={}".format(key, decoded_value))
        return decoded_value

    def delete(self, key):
        conn = self.get_connection()
        conn.delete(key)
