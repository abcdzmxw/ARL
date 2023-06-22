
from app import utils
from app.services.system.db_utils import get_db_utils
from app.services.system.uuid_utils import get_uuid
from app.utils import gen_md5
from app.utils.user import salt

db_utils = get_db_utils()

logger = utils.get_logger()


def user_page_list(args):
    """
    分页查询用户列表
    """
    page = args.pop("page", 1)
    size = args.pop("size", 10)
    username = args.pop("username")
    name = args.pop("name")

    # 执行分页查询
    query_sql = "SELECT user_id,name,username,email,phone FROM t_user WHERE 1=1 "

    condition = ""
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

    # 获取总条数
    query_total = db_utils.get_query_total(sql=count_query_sql)

    # 获取查询结果
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


def is_exist_user(username):
    """
    通过username查询是否存在此用户
    """
    # 查询总数
    count_query_sql = "SELECT count(*) FROM t_user WHERE username= %s "
    query_total = db_utils.get_query_total(sql=count_query_sql)

    # 获取记录数
    logger.info("query_total:{}".format(query_total))
    return query_total


def save_user(username, password, name, email=None, phone=None):
    """
    新增用户
    """
    logger.info("save_user方法执行插入菜单----username:{} password:{} name:{} email:{} phone:{}"
                .format(username, password, name, email, phone))

    # 生成用户id
    user_id = get_uuid()

    # 密码md5加密
    md5_password = gen_md5(salt + password)

    # 执行插入语句
    insert_sql = "INSERT INTO t_user (user_id, name, username, password, email, phone) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (user_id, name, username, md5_password, email, phone)
    db_utils.execute_insert(sql=insert_sql, args=values)

    return user_id


def get_by_user_id(user_id):
    """
    通过user_id查询用户信息 user_id是uuid
    """
    # 执行插入语句
    query_sql = "SELECT id, user_id,name,username,email,phone FROM t_user WHERE user_id=%s "
    user_list = db_utils.get_query_list(sql=query_sql, args=user_id)
    user = None
    if user_list:
        user = user_list[0]

    return user


def update_user(user_id, name, email=None, phone=None):
    """
    更新用户的信息
    """
    logger.info(
        "update_user方法执行更新用户信息----user_id:{},name:{} email:{} phone:{} ".format(user_id, name, email, phone))
    update_sql = "UPDATE t_user SET name = %s, email = %s, phone = %s WHERE user_id = %s"
    values = (name, email, phone, user_id)

    db_utils.execute_update(sql=update_sql, args=values)
    logger.info("update_user方法执行更新用户信息完成")


def delete_by_user_id(user_id):
    """
    通过user_id删除用户  user_id是uuid
    """
    query = "DELETE FROM t_user WHERE user_id = %s"
    db_utils.execute_update(sql=query, args=user_id)

