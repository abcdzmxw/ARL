import bson
import re
import pymysql
from app import utils
from dbutils.pooled_db import PooledDB

pool = PooledDB(
    creator=pymysql,  # 使用pymysql作为连接器
    host='192.168.1.101',
    user='root',
    password='Hjrtnbec*38',
    database='galaxy_arl',
    autocommit=True,  # 自动提交事务
    charset='utf8'  # 设置字符集
)

logger = utils.get_logger()


def save_menu(menu_name, menu_code, sort, parent_id, click_uri, route):
    logger.info("执行插入菜单----menu_name:{} menu_code:{} sort:{} parent_id:{} click_uri:{} route:{}".format(menu_name,
                                                                                                              menu_code,
                                                                                                              sort,
                                                                                                              parent_id,
                                                                                                              click_uri,
                                                                                                              route))

    # 创建数据库连接
    conn = pool.connection()

    # 创建游标对象
    cursor = conn.cursor()

    # 执行插入语句
    query = "INSERT INTO t_menu (menu_name, menu_code, click_uri, parent, sort, route) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (menu_name, menu_code, click_uri, parent_id, sort, route)
    cursor.execute(query, values)
    # 获取插入的ID
    inserted_id = cursor.lastrowid
    # 提交更改
    cnx.commit()
    logger.info("执行插入菜单完成----inserted_id:{}".format(inserted_id))

    # 关闭游标和数据库连接
    cursor.close()
    cnx.close()
    return inserted_id
