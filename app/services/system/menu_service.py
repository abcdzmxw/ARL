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


def get_by_id(menu_id):
    logger.info("通过菜单id查询菜单----menu_id:{}".format(menu_id))
    # 创建数据库连接
    conn = pool.connection()

    # 创建游标对象
    cursor = conn.cursor()

    # 执行查询语句
    query = "SELECT id,menu_name,menu_code, click_uri, parent, sort, route FROM t_menu WHERE id= %s "
    cursor.execute(query, menu_id)

    # 获取查询结果
    results = cursor.fetchall()

    # 好像是打印字段的属性
    index = cursor.description

    menu_obj = None
    # 处理查询结果
    for row in results:
        menu_obj = {}
        # 处理每一行数据
        for i in range(len(index)):
            # index[i][0] 获取字段里属性中的局部信息
            menu_obj[index[i][0]] = row[i]
    logger.info("通过菜单id查询菜单----menu_obj:{}".format(menu_obj))
    cursor.close()
    conn.close()

    return menu_obj


def is_exist_menu_code(menu_code):
    # 创建数据库连接
    conn = pool.connection()

    # 创建游标对象
    cursor = conn.cursor()

    # 执行插入语句
    query = "SELECT id,menu_name,menu_code, click_uri, parent, sort, route FROM t_menu WHERE menu_code= %s "
    cursor.execute(query, menu_code)

    # 获取查询结果
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    # 获取记录数
    logger.info("result:{}".format(result))

    if result is None:
        count = 0
    else:
        count = result[0]

    logger.info("count:{}".format(count))
    return count


def save_menu(menu_name, menu_code, sort, parent_id, click_uri, route):
    logger.info("save_menu方法执行插入菜单----menu_name:{} menu_code:{} sort:{} parent_id:{} click_uri:{} route:{}"
                .format(menu_name, menu_code, sort, parent_id, click_uri, route))

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
    logger.info("save_menu执行插入菜单完成----inserted_id:{}".format(inserted_id))

    # 关闭游标和数据库连接
    cursor.close()
    conn.close()
    return inserted_id


def update_menu(menu_id, menu_name, sort, parent_id, click_uri, route):
    logger.info("update_menu方法执行更新菜单----menu_id:{},menu_name:{} sort:{} parent_id:{} click_uri:{} route:{}"
                .format(menu_id, menu_name, sort, parent_id, click_uri, route))

    # 创建数据库连接
    conn = pool.connection()

    # 创建游标对象
    cursor = conn.cursor()

    # 执行插入语句
    query = "UPDATE t_menu SET menu_name = %s, click_uri = %s, parent = %s, sort = %s, route = %s WHERE id = %s"
    values = (menu_name, click_uri, parent_id, sort, route, menu_id)
    cursor.execute(query, values)

    # 提交更改
    conn.commit()
    logger.info("update_menu方法执行更新菜单完成")

    # 关闭游标和数据库连接
    cursor.close()
    conn.close()


def delete_menu_by_id(menu_id):
    # 创建数据库连接
    conn = pool.connection()

    # 创建游标对象
    cursor = conn.cursor()

    query = "DELETE FROM t_menu WHERE id = %s"
    cursor.execute(query, menu_id)

    # 提交更改
    conn.commit()

    # 关闭游标和数据库连接
    cursor.close()
    conn.close()


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
        # 处理每一行数据
        obj = {}
        for i in range(len(index)):
            # index[i][0] 获取字段里属性中的局部信息
            obj[index[i][0]] = row[i]
        if obj["parent"] is not None:
            obj["parent_dto"] = get_by_id(obj["parent"])

        menu_list.append(obj)

    # 关闭游标和数据库连接
    cursor.close()
    conn.close()

    total_pages = (query_total + size - 1) // size
    logger.info("query_total:{}, size={}, page={}, total_pages={}, menu_list={}".format(query_total, size, page,
                                                                                        total_pages, menu_list))
    result = {
        "page": page,
        "size": size,
        "total": query_total,
        "items": menu_list
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

    menu_map = {}  # 创建空的菜单字典

    menus = []
    for menu in menu_list:
        parent = menu["parent"]
        if parent is None:
            menus.append(menu)
        else:
            a_list = menu_map.get(parent)
            if a_list is None:
                a_list = []
            a_list.append(menu)
            menu_map[parent] = a_list

    for menu in menus:
        secondMenuList = menu_map[menu["id"]]
        if secondMenuList is not None:
            sorted_list = sorted(secondMenuList, key=lambda x: x.sort)
            menus["secondMenuList"] = sorted_list

    result_list = sorted(menus, key=lambda x: x.sort)

    logger.info("query:{}, username:{},resutl_list:{}".format(query, username, result_list))
    return result_list


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
