from app import utils
from app.services.system.db_utils import get_db_utils

db_utils = get_db_utils()
logger = utils.get_logger()


def get_by_role_id(role_id):
    """
    通过role_id查询角色对象
    """
    logger.info("开始查询get_by_role_id  role_id:{}".format(role_id))
    # 执行插入语句
    query_sql = "SELECT id, role_name,role_code FROM t_role WHERE id=%s "
    role = db_utils.get_one(sql=query_sql, args=role_id)
    return role


def get_by_role_code(role_code):
    """
    通过role_code查询角色对象
    """
    query_sql = "SELECT id, role_name,role_code FROM t_role WHERE role_code=%s "
    role = db_utils.get_one(sql=query_sql, args=role_code)
    return role


def save_role(role_name, role_code):
    """
    保存角色对象
    """
    # 执行插入语句
    insert_sql = "INSERT INTO t_role (role_name, role_code) VALUES (%s, %s)"
    values = (role_name, role_code)
    db_utils.execute_insert(sql=insert_sql, args=values)


def role_page_list(args):
    """
    分页查询角色列表
    """
    page = args.pop("page", 1)
    size = args.pop("size", 10)
    role_name = args.pop("role_name")
    role_code = args.pop("role_code")

    # 执行分页查询
    query_sql = "SELECT id,role_name,role_code FROM t_role WHERE 1=1 "

    condition = ""
    # 如果条件存在，则添加条件到查询语句
    if role_name:
        condition += " AND role_name LIKE '%{}%'".format(role_name)

    if role_code:
        condition += " AND role_code LIKE '%{}%'".format(role_code)

    count_query_sql = " SELECT COUNT(*) FROM t_role WHERE 1=1 " + condition
    query_sql += condition
    # 计算查询的起始位置
    offset = (page - 1) * size
    query_sql += " LIMIT " + str(size) + " OFFSET " + str(offset)
    # 获取总条数
    query_total = db_utils.get_query_total(sql=count_query_sql)
    user_list = db_utils.get_query_list(sql=query_sql)

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


def update_role(role_id, role_name):
    """
    通过rle_id来更新角色名称
    """
    update_sql = "UPDATE t_role SET role_name = %s WHERE id = %s"
    values = (role_name, role_id)
    db_utils.execute_update(sql=update_sql, args=values)


def delete_by_role_id(role_id):
    """
    删除角色
    """
    query = "DELETE FROM t_role WHERE id = %s"
    db_utils.execute_update(sql=query, args=role_id)


def save_user_role(user_id, role_id_str):
    """
    保存用户角色关系
    """
    role_id_array = role_id_str.split(',')
    values = [(user_id, role_id) for role_id in role_id_array]

    logger.info("save_user_role  user_id:{},values={}".format(user_id, values))
    # 执行插入语句
    insert_sql = "INSERT INTO t_user_role (user_id, role_id) VALUES (%s, %s)"
    db_utils.execute_executemany_insert(sql=insert_sql, args=values)
    logger.info("save_user_role  执行完成.....")


def delete_user_role(user_id):
    """
    删除用户据说关系
    """
    query = "DELETE FROM t_user_role WHERE user_id = %s"
    db_utils.execute_update(sql=query, args=user_id)


def get_user_role_list(username):
    """
    查询用户的角色列表
    """
    logger.info("get_user_menu_list,username:{}".format(username))
    # 执行分页查询
    query = "SELECT r.id, r.role_name,r.role_code FROM t_role r JOIN t_user_role ur ON r.id=ur.role_id " \
            "JOIN t_user u ON ur.user_id=u.id WHERE username=%s"

    role_list = db_utils.get_query_list(sql=query, args=username)
    return role_list
