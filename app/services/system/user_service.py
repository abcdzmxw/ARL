import pymysql

from app import utils
from dbutils.pooled_db import PooledDB

pool = PooledDB(
    creator=pymysql,  # 使用pymysql作为连接器
    host='192.168.1.100',
    user='root',
    password='Hjrtnbec*38',
    database='galaxy_arl',
    maxconnections=10,  # 连接池大小
    autocommit=True,  # 自动提交事务
    charset='utf8'  # 设置字符集
)

logger = utils.get_logger()


def user_page_list(args):
    page = args.pop("page", 1)
    size = args.pop("size", 10)
    username = args.pop("username")
    name = args.pop("name")

    # 执行分页查询
    query_sql = "SELECT user_id,name,username,email,phone FROM t_user WHERE 1=1 "

    condition = "";
    # 如果条件存在，则添加条件到查询语句
    if username:
        condition += " AND username LIKE '%{}%'".format(username)

    if name:
        condition += " AND name LIKE '%{}%'".format(name)

    count_query_sql = " SELECT COUNT(*) FROM t_user WHERE 1=1 " + condition
    query_sql = query_sql + condition
    # 计算查询的起始位置
    offset = (page - 1) * size
    query_sql += " LIMIT " + str(size) + " OFFSET " + str(offset)
    # 创建数据库连接
    conn = pool.connection()

    cursor = conn.cursor()
    cursor.execute(count_query_sql)

    # 获取总条数
    query_total = cursor.fetchone()[0]

    cursor.execute(query_sql)

    # 获取查询结果
    results = cursor.fetchall()

    user_list = []

    # 好像是打印字段的属性
    index = cursor.description

    # 处理查询结果
    for row in results:
        # 处理每一行数据
        obj = {}
        for i in range(len(index)):
            # index[i][0] 获取字段里属性中的局部信息
            obj[index[i][0]] = row[i]

        user_list.append(obj)

    # 关闭游标和数据库连接
    cursor.close()
    conn.close()

    total_pages = (query_total + size - 1) // size
    logger.info("query_total:{}, size={}, page={}, total_pages={}, menu_list={}".format(query_total, size, page,
                                                                                        total_pages, user_list))
    result = {
        "page": page,
        "size": size,
        "total": query_total,
        "items": user_list
    }

    return result


def get_menu_by_role_id(role_id):
    logger.info("get_menu_by_role_id:, role_id:{}".format(role_id))
    # 执行分页查询
    query = "SELECT m.id,m.menu_name,m.menu_code, m.click_uri, m.parent, m.sort, m.route FROM t_menu m JOIN t_role_menu rm ON m.id=rm.menu_id JOIN t_role r ON rm.role_id=r.id WHERE r.id=%s"
    logger.info("query:{}, role_id:{}".format(query, role_id))
    # 创建数据库连接
    conn = pool.connection()
    cursor = conn.cursor()
    logger.info("准备执行。。。。。。")
    cursor.execute(query, role_id)
    logger.info("准备完成。。。。。。")
    # 获取查询结果
    results = cursor.fetchall()
    menu_list = []
    logger.info("query:{}, role_id:{}".format(query, role_id))
    # 好像是打印字段的属性
    index = cursor.description

    # 处理查询结果
    for row in results:
        # 处理每一行数据
        obj = {}
        for i in range(len(index)):
            # index[i][0] 获取字段里属性中的局部信息
            obj[index[i][0]] = row[i]

        menu_list.append(obj)

    # 关闭游标和数据库连接
    cursor.close()
    conn.close()
    logger.info("query:{}, role_id:{},menu_list:{}".format(query, role_id, menu_list))
    return menu_list


def get_user_menu_list(username):
    logger.info("get_user_menu_list,username:{}".format(username))
    # 执行分页查询
    query = "SELECT m.id,m.menu_name,m.menu_code, m.click_uri, m.parent, m.sort, m.route FROM t_menu m JOIN t_role_menu rm ON m.id=rm.menu_id JOIN t_role r ON rm.role_id=r.id JOIN t_user_role ur ON r.id=ur.role_id JOIN t_user u ON ur.user_id=u.id WHERE u.username=%s"
    logger.info("query:{}, username:{}".format(query, username))
    # 创建数据库连接
    conn = pool.connection()
    cursor = conn.cursor()
    logger.info("准备执行。。。。。。")
    cursor.execute(query, username)
    logger.info("准备完成。。。。。。")
    # 获取查询结果
    results = cursor.fetchall()
    menu_list = []
    # 好像是打印字段的属性
    index = cursor.description

    # 处理查询结果
    for row in results:
        # 处理每一行数据
        obj = {}
        for i in range(len(index)):
            # index[i][0] 获取字段里属性中的局部信息
            obj[index[i][0]] = row[i]

        menu_list.append(obj)

    # 关闭游标和数据库连接
    cursor.close()
    conn.close()
    logger.info("query:{}, username:{},menu_list:{}".format(query, username, menu_list))
    return menu_list


def get_first_level_menu_list():
    # 执行分页查询
    query = "SELECT m.id,m.menu_name,m.menu_code, m.click_uri, m.parent, m.sort, m.route FROM t_menu m WHERE m.parent IS NULL ORDER BY m.sort"
    # 创建数据库连接
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(query)
    # 获取查询结果
    results = cursor.fetchall()
    menu_list = []
    # 好像是打印字段的属性
    index = cursor.description

    # 处理查询结果
    for row in results:
        # 处理每一行数据
        obj = {}
        for i in range(len(index)):
            # index[i][0] 获取字段里属性中的局部信息
            obj[index[i][0]] = row[i]

        menu_list.append(obj)

    # 关闭游标和数据库连接
    cursor.close()
    conn.close()
    logger.info("get_first_level_menu_list query:{}, menu_list:{}".format(query, menu_list))
    return menu_list
