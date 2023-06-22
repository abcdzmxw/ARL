import threading
import redis
from redis import ConnectionPool
from app.utils import get_logger

logger = get_logger()


class RedisLock(threading.Lock):
    def __enter__(self):
        logger.info("获取锁。。。。。。")
        self.acquire()

    def __exit__(self, exc_type, exc_value, traceback):
        logger.info("释放锁。。。。。。")
        self.release()


# 创建锁对象
redis_lock = RedisLock()


class RedisUtils:
    _initialized = False

    def __init__(self, host='localhost', port=6379, password=None, db=0, max_connections=10):
        logger.info("RedisUtils初始化----host:{},port={},password={}".format(host, port, password))
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
        logger.info("redis获取值,key={}, value={}".format(key, decoded_value))
        return decoded_value

    def delete(self, key):
        conn = self.get_connection()
        conn.delete(key)

    def is_initialized(self):
        return self._initialized


# 模块级别的变量，用于存储全局实例
redis_obj = None


def get_redis_utils():
    global redis_obj
    if not redis_obj or not redis_obj.is_initialized():
        with redis_lock:
            if not redis_obj or not redis_obj.is_initialized():
                redis_obj = RedisUtils(host='154.39.246.13', port=6379, password='HRwOi8vcy5uYS1j', db=0)
                redis_obj._initialized = True
                logger.info("初始化成功。。。。。。{}".format(redis_obj))
    return redis_obj
