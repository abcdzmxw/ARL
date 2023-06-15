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
    maxconnections=10,  # 连接池大小
    autocommit=True,  # 自动提交事务
    charset='utf8'  # 设置字符集
)

logger = utils.get_logger()


class MenuDto:
    def __init__(self, id, menu_name, menu_code, click_uri, parent, sort, route):
        self.id = id
        self.menu_name = menu_name
        self.menu_code = menu_code
        self.click_uri = click_uri
        self.parent = parent
        self.sort = sort
        self.route = route


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
    conn.commit()
    logger.info("执行插入菜单完成----inserted_id:{}".format(inserted_id))

    # 关闭游标和数据库连接
    cursor.close()
    conn.close()
    return inserted_id


def menu_page_list(args):
    page = args.pop("page", 1)
    size = args.pop("size", 10)
    menu_name = args.pop("menu_name")
    menu_code = args.pop("menu_code")
    route = args.pop("route")

    # 执行分页查询
    query = "SELECT id,menu_name,menu_code, click_uri, parent, sort, route FROM t_menu WHERE 1=1 "

    # 如果条件存在，则添加条件到查询语句
    if menu_name:
        query += " AND menu_name LIKE '%{}%'".format(menu_name)

    if menu_code:
        query += " AND menu_code LIKE '%{}%'".format(menu_code)

    if route:
        query += " AND route LIKE '%{}%'".format(route)

    query += " LIMIT %s OFFSET %s "

    # 计算查询的起始位置
    offset = (page - 1) * size

    values = (size, offset)

    # 创建数据库连接
    conn = pool.connection()

    cursor = conn.cursor()

    cursor.execute(query, values)

    # 获取查询结果
    results = cursor.fetchall()

    return results
    # menu_list = []
    # # 处理查询结果
    # for row in results:
    #     # 处理每一行数据
    #     menuDto = MenuDto(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
    #     menu_list.append(menuDto)
    #
    # # 关闭游标和数据库连接
    # cursor.close()
    # conn.close()
    #
    # return menu_list
