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


class ResultDto:
    def __init__(self, records=None, total=None, size=None, current=None, pages=None):
        self.records = records
        self.total = total
        self.size = size
        self.current = current
        self.pages = pages


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

    count_query_sql = query

    # 计算查询的起始位置
    offset = (page - 1) * size
    query += " LIMIT " + str(size) + " OFFSET " + str(offset)
    # 创建数据库连接
    conn = pool.connection()

    cursor = conn.cursor()
    query_total = cursor.execute(count_query_sql)

    cursor.execute(query)

    # 获取查询结果
    results = cursor.fetchall()

    menu_list = []

    # 好像是打印字段的属性
    index = cursor.description

    # 处理查询结果
    for row in results:
        logger.info(
            "执行插入菜单----id:{} menu_name:{} menu_code:{} sort:{} parent_id:{} click_uri:{} route:{}".format(row[0],
                                                                                                                row[1],
                                                                                                                row[2],
                                                                                                                row[3],
                                                                                                                row[4],
                                                                                                                row[5],
                                                                                                                row[6]))
        # 处理每一行数据
        obj = {}
        for i in range(len(index)):
            # index[i][0] 获取字段里属性中的局部信息
            obj[index[i][0]] = row[i]
        menu_list.append(obj)

    # 关闭游标和数据库连接
    cursor.close()
    conn.close()

    try:
        total_pages = (query_total + size - 1) // size
        logger.info("query_total:{}, size={}, page={}, total_pages={}, menu_list={}".format(query_total, size, page,
                                                                                            total_pages, menu_list))
        # 可能会引发异常的代码
        result = ResultDto(records=menu_list, total=query_total, size=size, current=page, pages=total_pages)
    except Exception as e:
        # 捕获异常并打印异常信息
        logger.error("An error occurred: {}".format(e))

    logger.info("result:{}".format(result))
    return result
