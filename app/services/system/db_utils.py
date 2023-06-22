import threading

import pymysql
from dbutils.pooled_db import PooledDB

from app.utils import get_logger


class DatabaseUtils:
    _instance = None
    _initialized = False
    _lock = threading.Lock()

    def __init__(self, host='localhost', user='root', password='', database='', max_connections=10):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.max_connections = max_connections
        self.connection_pool = None
        self.connect()

    def connect(self):
        self.connection_pool = PooledDB(
            creator=pymysql,
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            maxconnections=self.max_connections
        )

    def get_connection(self):
        return self.connection_pool.connection()

    def get_query_list(self, sql, args=None):
        """
        执行sql,返回查询数据列表
        """
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, args)
                results = cursor.fetchall()
                # 字段的属性
                index = cursor.description
                data_list = []

                # 处理查询结果
                for row in results:
                    obj = {}
                    # 处理每一行数据
                    for i in range(len(index)):
                        # index[i][0] 获取字段里属性中的局部信息
                        obj[index[i][0]] = row[i]
                    data_list.append(obj)

                return data_list
        finally:
            conn.close()

    def get_query_total(self, sql, args=None):
        """
        执行sql,返回查询数据总数
        """
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, args)
                # 获取总条数
                query_total = cursor.fetchone()[0]
                return query_total
        finally:
            conn.close()

    def execute_update(self, sql, args=None):
        """
        执行更新sql
        """
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, args)
                conn.commit()
        finally:
            conn.close()

    def execute_insert(self, sql, args=None):
        """
        执行插入sql
        """
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, args)
                conn.commit()
        finally:
            conn.close()

    @classmethod
    def instance(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = cls(*args, **kwargs)
        return cls._instance


logger = get_logger()

# 创建全局 DatabaseUtils 对象
db_utils = None
# 创建锁对象
db_lock = threading.Lock()


def get_db_utils():
    global db_utils
    if db_utils is None:
        with db_lock:
            if db_utils is None:
                db_utils = DatabaseUtils.instance(
                    host='192.168.1.100',
                    user='root',
                    password='Hjrtnbec*38',
                    database='galaxy_arl',
                    maxconnections=10,
                    autocommit=True,
                    charset='utf8'
                )
                db_utils._initialized = True
    return db_utils
