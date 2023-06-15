import bson
import re
import MySQLdb
from app import utils

logger = utils.get_logger()


def save_menu(menu_name, menu_code, sort, parent_id, click_uri, route):
    logger.info("执行插入菜单----menu_name:{} menu_code:{} sort:{} parent_id:{} click_uri:{} route:{}".format(menu_name,
                                                                                                              menu_code,
                                                                                                              sort,
                                                                                                              parent_id,
                                                                                                              click_uri,
                                                                                                              route))

    # 创建数据库连接
    cnx = MySQLdb.connect(
        host='154.39.246.13',
        user='test',
        password='Aa*bc#1s2g3',
        database='galaxy_arl'
    )

    # 创建游标对象
    cursor = cnx.cursor()

    # 执行插入语句
    query = "INSERT INTO person (menu_name, menu_code, click_uri, parent, sort, route) VALUES (%s, %s, %s, %s, %s, %s)"
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
