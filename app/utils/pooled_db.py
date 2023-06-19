import pymysql
from dbutils.pooled_db import PooledDB


class DatabasePool:
    def __init__(self):
        self.pool = None

    def initialize(self):
        if self.pool is None:
            self.pool = PooledDB(
                creator=pymysql,  # 使用pymysql作为连接器
                host='192.168.1.100',
                user='root',
                password='Hjrtnbec*38',
                database='galaxy_arl',
                maxconnections=10,  # 连接池大小
                autocommit=True,  # 自动提交事务
                charset='utf8'  # 设置字符集
            )

    def get_connection(self):
        if self.pool is None:
            raise Exception("Database pool is not initialized")

        return self.pool.connection()


# 创建一个全局的数据库连接池对象
db_pool = DatabasePool()
