import pymysql
from dbutils.pooled_db import PooledDB


class DBPool:
    _instance = None

    def __new__(cls, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.pool = PooledDB(
                creator=pymysql,  # 使用pymysql作为连接器
                host='192.168.1.100',
                user='root',
                password='Hjrtnbec*38',
                database='galaxy_arl',
                maxconnections=10,  # 连接池大小
                autocommit=True,  # 自动提交事务
                charset='utf8'  # 设置字符集
            )
        return cls._instance

    @classmethod
    def get_connection(cls):
        return cls._instance.pool.connection()
