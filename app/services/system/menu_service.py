
from app import utils
from app.services.system.db_utils import get_db_utils

db_utils = get_db_utils()
logger = utils.get_logger()


def get_by_id(menu_id):
    logger.info("通过菜单id查询菜单----menu_id:{}".format(menu_id))
    # 执行查询语句
    query = "SELECT id,menu_name,menu_code, click_uri, parent, sort, route FROM t_menu WHERE id= %s "
    menu_obj = db_utils.get_one(sql=query, args=menu_id)
    return menu_obj


def is_exist_menu_code(menu_code):
    query = "SELECT id,menu_name,menu_code, click_uri, parent, sort, route FROM t_menu WHERE menu_code= %s "
    total_count = db_utils.get_query_total(sql=query, args=menu_code)
    logger.info("total_count:{}".format(total_count))
    return total_count


def save_menu(menu_name, menu_code, sort, parent_id, click_uri, route):
    logger.info("save_menu方法执行插入菜单----menu_name:{} menu_code:{} sort:{} parent_id:{} click_uri:{} route:{}"
                .format(menu_name, menu_code, sort, parent_id, click_uri, route))
    # 执行插入语句
    insert_sql = "INSERT INTO t_menu (menu_name, menu_code, click_uri, parent, sort, route) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (menu_name, menu_code, click_uri, parent_id, sort, route)
    db_utils.execute_insert(sql=insert_sql, args=values)
    logger.info("save_menu执行插入菜单完成----")



def update_menu(menu_id, menu_name, sort, parent_id, click_uri, route):
    logger.info("update_menu方法执行更新菜单----menu_id:{},menu_name:{} sort:{} parent_id:{} click_uri:{} route:{}"
                .format(menu_id, menu_name, sort, parent_id, click_uri, route))
    # 执行插入语句
    update_sql = "UPDATE t_menu SET menu_name = %s, click_uri = %s, parent = %s, sort = %s, route = %s WHERE id = %s"
    values = (menu_name, click_uri, parent_id, sort, route, menu_id)
    db_utils.execute_update(sql=update_sql, args=values)
    logger.info("update_menu方法执行更新菜单完成")


def delete_menu_by_id(menu_id):
    delete_sql = "DELETE FROM t_menu WHERE id = %s"
    db_utils.execute_update(sql=delete_sql, args=menu_id)


def menu_page_list(args):
    page = args.pop("page", 1)
    size = args.pop("size", 10)
    menu_name = args.pop("menu_name")
    menu_code = args.pop("menu_code")
    route = args.pop("route")

    # 执行分页查询
    query_sql = "SELECT id,menu_name,menu_code, click_uri, parent, sort, route FROM t_menu WHERE 1=1 "

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

    query_total = db_utils.get_query_total(sql=count_query_sql)
    menu_list = db_utils.get_query_list(sql=query_sql)
    for menu in menu_list:
        if menu["parent"] is not None:
            menu["parent_dto"] = get_by_id(menu["parent"])

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
    menu_list = db_utils.get_query_list(sql=query, args=role_id)
    logger.info("query:{}, role_id:{},menu_list:{}".format(query, role_id, menu_list))
    return menu_list


def get_user_menu_list(username):
    logger.info("get_user_menu_list,username:{}".format(username))
    # 执行分页查询
    query = "SELECT distinct m.id,m.menu_name,m.menu_code, m.click_uri, m.parent, m.sort, m.route FROM t_menu m JOIN t_role_menu rm ON m.id=rm.menu_id JOIN t_role r ON rm.role_id=r.id JOIN t_user_role ur ON r.id=ur.role_id JOIN t_user u ON ur.user_id=u.id WHERE u.username=%s"
    logger.info("query:{}, username:{}".format(query, username))
    menu_list = db_utils.get_query_list(sql=query, args=username)

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
            sorted_list = sorted(secondMenuList, key=lambda x: x['sort'])
            menu["secondMenuList"] = sorted_list

    result_list = sorted(menus, key=lambda x: x['sort'])

    logger.info("query:{}, username:{},result_list:{}".format(query, username, result_list))
    return result_list


def get_first_level_menu_list():
    # 执行分页查询
    query = "SELECT m.id,m.menu_name,m.menu_code, m.click_uri, m.parent, m.sort, m.route FROM t_menu m WHERE m.parent IS NULL ORDER BY m.sort"
    menu_list = db_utils.get_query_list(sql=query)
    logger.info("get_first_level_menu_list query:{}, menu_list:{}".format(query, menu_list))
    return menu_list
