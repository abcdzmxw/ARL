from flask import g

from app import utils
from app.services.system.db_utils import get_db_utils

db_utils = get_db_utils()
logger = utils.get_logger()


def get_by_id(menu_id):
    # 执行查询语句
    query_sql = "SELECT id,menu_name,menu_code, click_uri, parent_id, sort, route FROM t_menu WHERE id= %s "
    logger.info("get_by_id, query_sql={}, menu_id={}".format(query_sql, menu_id))
    menu_obj = db_utils.get_one(sql=query_sql, args=menu_id)
    return menu_obj


def is_exist_menu_code(menu_code):
    query_count_sql = "SELECT count(1) FROM t_menu WHERE menu_code= %s "
    logger.info("is_exist_menu_code, query_count_sql={}, menu_code={}".format(query_count_sql, menu_code))
    total_count = db_utils.get_query_total(sql=query_count_sql, args=menu_code)
    logger.info("total_count:{}".format(total_count))
    return total_count


def save_menu(menu_name, menu_code, sort, parent_id, click_uri, route):
    logger.info("save_menu方法执行插入菜单----menu_name:{} menu_code:{} sort:{} parent_id:{} click_uri:{} route:{}"
                .format(menu_name, menu_code, sort, parent_id, click_uri, route))
    current_user = g.get('current_user')
    # 执行插入语句
    insert_sql = "INSERT INTO t_menu (menu_name, menu_code, click_uri, parent_id, sort, route, created_by) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (menu_name, menu_code, click_uri, parent_id, sort, route, current_user)
    logger.info("save_menu, insert_sql={}, values={}".format(insert_sql, values))
    db_utils.execute_insert(sql=insert_sql, args=values)
    logger.info("save_menu执行插入菜单完成----")


def update_menu(menu_id, menu_name, sort, parent_id, click_uri, route):
    logger.info("update_menu方法执行更新菜单----menu_id:{},menu_name:{} sort:{} parent_id:{} click_uri:{} route:{}"
                .format(menu_id, menu_name, sort, parent_id, click_uri, route))
    current_user = g.get('current_user')
    # 执行插入语句
    update_sql = "UPDATE t_menu SET menu_name = %s, click_uri = %s, parent_id = %s, sort = %s, route = %s, updated_at=NOW(), updated_by=%s WHERE id = %s"
    values = (menu_name, click_uri, parent_id, sort, route, current_user, menu_id)
    logger.info("update_menu, update_sql={}, values={}".format(update_sql, values))
    db_utils.execute_update(sql=update_sql, args=values)
    logger.info("update_menu方法执行更新菜单完成")


def delete_menu_by_id(menu_id):
    delete_sql = "DELETE FROM t_menu WHERE id = %s"
    logger.info("delete_menu_by_id, delete_sql={}, menu_id={}".format(delete_sql, menu_id))
    db_utils.execute_update(sql=delete_sql, args=menu_id)


def delete_role_menu_by_role_id(role_id):
    delete_sql = "DELETE FROM t_role_menu WHERE role_id = %s"
    logger.info("delete_role_menu_by_role_id, delete_sql={}, role_id={}".format(delete_sql, role_id))
    db_utils.execute_update(sql=delete_sql, args=role_id)


def save_role_menu(role_id, menu_id_str):
    """
    保存角色菜单关系
    """
    current_user = g.get('current_user')
    menu_id_array = menu_id_str.split(',')
    values = [(role_id, menu_id, current_user) for menu_id in menu_id_array]

    logger.info("save_role_menu  values={}".format(values))
    # 执行插入语句
    insert_sql = "INSERT INTO t_role_menu (role_id, menu_id, created_by) VALUES (%s, %s, %s)"
    logger.info("save_role_menu, insert_sql={}, values={}".format(insert_sql, values))
    db_utils.execute_executemany_insert(sql=insert_sql, args=values)
    logger.info("save_role_menu  执行完成.....")


def menu_page_list(args):
    page = args.pop("page", 1)
    size = args.pop("size", 10)
    menu_name = args.pop("menu_name")
    menu_code = args.pop("menu_code")
    route = args.pop("route")

    # 执行分页查询
    query_sql = "SELECT id,menu_name,menu_code, click_uri, parent_id, sort, route FROM t_menu WHERE 1=1 "

    condition = ""
    # 如果条件存在，则添加条件到查询语句
    if menu_name:
        condition += " AND menu_name LIKE '%{}%'".format(menu_name)

    if menu_code:
        condition += " AND menu_code LIKE '%{}%'".format(menu_code)

    if route:
        condition += " AND route LIKE '%{}%'".format(route)

    query_sql = query_sql + condition
    count_query_sql = " SELECT COUNT(*) FROM t_menu WHERE 1=1 " + condition
    # 计算查询的起始位置
    offset = (page - 1) * size
    query_sql += " LIMIT " + str(size) + " OFFSET " + str(offset)
    logger.info("menu_page_list, count_query_sql={}, query_sql={}".format(count_query_sql, query_sql))
    query_total = db_utils.get_query_total(sql=count_query_sql)
    menu_list = db_utils.get_query_list(sql=query_sql)
    for menu in menu_list:
        if menu["parent_id"] is not None:
            menu["parent_dto"] = get_by_id(menu["parent_id"])

    result = {
        "page": page,
        "size": size,
        "total": query_total,
        "items": menu_list
    }

    return result


def menu_list():
    # 执行分页查询
    query_sql = "SELECT id,menu_name,menu_code, click_uri, parent_id, sort, route FROM t_menu WHERE 1=1 "
    menu_list = db_utils.get_query_list(sql=query_sql)

    menu_map = {}  # 创建空的菜单字典

    menus = []
    for menu in menu_list:
        parent_id = menu["parent_id"]
        if parent_id is None:
            menus.append(menu)
        else:
            a_list = menu_map.get(parent_id)
            if a_list is None:
                a_list = []
            a_list.append(menu)
            menu_map[parent_id] = a_list

    for menu in menus:
        secondMenuList = menu_map.get(menu["id"])
        logger.info("secondMenuList:{}".format(secondMenuList))
        if secondMenuList is not None:
            sorted_list = sorted(secondMenuList, key=lambda x: x['sort'])
            menu["childrens"] = sorted_list

    result_list = sorted(menus, key=lambda x: x['sort'])

    return result_list


def get_menu_by_role_id(role_id):
    logger.info("get_menu_by_role_id:, role_id:{}".format(role_id))
    # 执行分页查询
    query_sql = "SELECT m.id,m.menu_name,m.menu_code, m.click_uri, m.parent_id, m.sort, m.route FROM t_menu m JOIN t_role_menu rm ON m.id=rm.menu_id JOIN t_role r ON rm.role_id=r.id WHERE r.id=%s"
    logger.info("get_menu_by_role_id, query_sql={}, role_id={}".format(query_sql, role_id))
    menu_list = db_utils.get_query_list(sql=query_sql, args=role_id)
    return menu_list


def get_user_menu_list(username):
    logger.info("get_user_menu_list,username:{}".format(username))
    # 执行分页查询
    query_sql = "SELECT distinct m.id,m.menu_name,m.menu_code, m.click_uri, m.parent_id, m.sort, m.route FROM t_menu m JOIN t_role_menu rm ON m.id=rm.menu_id JOIN t_role r ON rm.role_id=r.id JOIN t_user_role ur ON r.id=ur.role_id JOIN t_user u ON ur.user_id=u.id WHERE u.username=%s"

    logger.info("get_user_menu_list, query_sql={}, username={}".format(query_sql, username))
    menu_list = db_utils.get_query_list(sql=query_sql, args=username)

    menu_map = {}  # 创建空的菜单字典

    menus = []
    for menu in menu_list:
        parent_id = menu["parent_id"]
        if parent_id is None:
            menus.append(menu)
        else:
            a_list = menu_map.get(parent_id)
            if a_list is None:
                a_list = []
            a_list.append(menu)
            menu_map[parent_id] = a_list

    for menu in menus:
        secondMenuList = menu_map.get(menu["id"])
        logger.info("secondMenuList:{}".format(secondMenuList))
        if secondMenuList is not None:
            sorted_list = sorted(secondMenuList, key=lambda x: x['sort'])
            menu["secondMenuList"] = sorted_list

    result_list = sorted(menus, key=lambda x: x['sort'])

    return result_list


def get_first_level_menu_list():
    # 执行分页查询
    query_sql = "SELECT m.id,m.menu_name,m.menu_code, m.click_uri, m.parent_id, m.sort, m.route FROM t_menu m WHERE m.parent_id IS NULL ORDER BY m.sort"
    logger.info("get_first_level_menu_list, query_sql={}".format(query_sql))
    menu_list = db_utils.get_query_list(sql=query_sql)
    return menu_list
