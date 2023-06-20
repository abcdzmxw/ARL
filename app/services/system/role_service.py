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


def get_by_role_id(role_id):
    """
    通过role_id查询角色对象
    """
    # 创建数据库连接
    conn = pool.connection()

    # 创建游标对象
    cursor = conn.cursor()
    logger.info("开始查询get_by_role_id  role_id:{}".format(role_id))
    # 执行插入语句
    query_sql = "SELECT id, role_name,role_code FROM t_role WHERE id=%s "
    cursor.execute(query_sql, role_id)
    # 获取查询结果
    results = cursor.fetchall()

    # 好像是打印字段的属性
    index = cursor.description
    obj = {}
    # 处理查询结果
    for row in results:
        # 处理每一行数据
        for i in range(len(index)):
            # index[i][0] 获取字段里属性中的局部信息
            obj[index[i][0]] = row[i]

    cursor.close()
    conn.close()

    # 获取记录数
    logger.info("get_by_role_id  role_id:{},obj={}".format(role_id, obj))
    if obj:
        return obj

    return None


def get_by_role_code(role_code):
    """
    通过role_code查询角色对象
    """
    # 创建数据库连接
    conn = pool.connection()

    # 创建游标对象
    cursor = conn.cursor()

    # 执行插入语句
    query_sql = "SELECT id, role_name,role_code FROM t_role WHERE role_code=%s "
    cursor.execute(query_sql, role_code)
    # 获取查询结果
    results = cursor.fetchall()

    # 好像是打印字段的属性
    index = cursor.description

    obj = {}
    # 处理查询结果
    for row in results:
        # 处理每一行数据
        for i in range(len(index)):
            # index[i][0] 获取字段里属性中的局部信息
            obj[index[i][0]] = row[i]

    cursor.close()
    conn.close()

    # 获取记录数
    logger.info("result:{}".format(obj))
    if obj:
        return obj

    return None


def save_role(role_name, role_code):
    """
    保存角色对象
    """
    # 创建数据库连接
    conn = pool.connection()

    # 创建游标对象
    cursor = conn.cursor()
    # 执行插入语句
    insert_sql = "INSERT INTO t_role (role_name, role_code) VALUES (%s, %s)"
    values = (role_name, role_code)
    cursor.execute(insert_sql, values)

    # 提交更改
    conn.commit()

    # 关闭游标和数据库连接
    cursor.close()
    conn.close()


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
        condition += " AND name LIKE '%{}%'".format(role_code)

    count_query_sql = " SELECT COUNT(*) FROM t_role WHERE 1=1 " + condition
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


def update_role(role_id, role_name):
    """
    通过rle_id来更新角色名称
    """
    # 创建数据库连接
    conn = pool.connection()

    # 创建游标对象
    cursor = conn.cursor()

    update_sql = "UPDATE t_role SET role_name = %s WHERE user_id = %s"
    values = (role_name, role_id)
    cursor.execute(update_sql, values)

    # 提交更改
    conn.commit()
    logger.info("update_role方法执行更新用户信息完成")

    # 关闭游标和数据库连接
    cursor.close()
    conn.close()


def delete_by_role_id(role_id):
    """
    删除角色
    """
    # 创建数据库连接
    conn = pool.connection()

    # 创建游标对象
    cursor = conn.cursor()

    query = "DELETE FROM t_role WHERE role_id = %s"
    cursor.execute(query, role_id)

    # 提交更改
    conn.commit()

    # 关闭游标和数据库连接
    cursor.close()
    conn.close()


def save_user_role(user_id, role_id_str):
    """
    保存用户角色关系
    """
    role_id_array = role_id_str.split(',')
    # 创建数据库连接
    conn = pool.connection()
    values = [(user_id, role_id) for role_id in role_id_array]
    # 创建游标对象
    cursor = conn.cursor()
    logger.info("save_user_role  user_id:{},values={}".format(user_id, values))
    # 执行插入语句
    insert_sql = "INSERT INTO t_user_role (user_id, role_id) VALUES (%s, %s)"
    cursor.executemany(insert_sql, values)
    logger.info("save_user_role  执行完成.....")
    # 提交更改
    conn.commit()
    cursor.close()
    conn.close()


def delete_user_role(user_id):
    """
    删除用户据说关系
    """
    # 创建数据库连接
    conn = pool.connection()

    # 创建游标对象
    cursor = conn.cursor()

    query = "DELETE FROM t_user_role WHERE user_id = %s"
    cursor.execute(query, user_id)

    # 提交更改
    conn.commit()

    # 关闭游标和数据库连接
    cursor.close()
    conn.close()


def get_user_role_list(username):
    """
    查询用户的角色列表
    """
    logger.info("get_user_menu_list,username:{}".format(username))
    # 执行分页查询
    query = "SELECT r.id, r.role_name,r.role_code FROM t_role r JOIN t_user_role ur ON r.id=ur.role_id " \
            "JOIN t_user u ON ur.user_id=u.id WHERE username=%s"

    # 创建数据库连接
    conn = pool.connection()
    cursor = conn.cursor()
    logger.info("准备执行。。。。。。")
    cursor.execute(query, username)
    logger.info("准备完成。。。。。。")
    # 获取查询结果
    results = cursor.fetchall()
    role_list = []
    # 好像是打印字段的属性
    index = cursor.description

    # 处理查询结果
    for row in results:
        # 处理每一行数据
        obj = {}
        for i in range(len(index)):
            # index[i][0] 获取字段里属性中的局部信息
            obj[index[i][0]] = row[i]

        role_list.append(obj)

    # 关闭游标和数据库连接
    cursor.close()
    conn.close()
    logger.info("query:{}, username:{},role_list:{}".format(query, username, role_list))
    return role_list
