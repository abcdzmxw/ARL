import pymysql
import uuid
from app import utils
from dbutils.pooled_db import PooledDB

from app.utils import gen_md5
from app.utils.user import salt

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


def is_exist_user(username):
    """
    通过username查询是否存在此用户
    """
    # 创建数据库连接
    conn = pool.connection()

    # 创建游标对象
    cursor = conn.cursor()

    # 执行插入语句
    count_query_sql = "SELECT count(*) FROM t_user WHERE username= %s "
    cursor.execute(count_query_sql, username)
    query_total = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    # 获取记录数
    logger.info("query_total:{}".format(query_total))
    return query_total


def save_user(username, password, name, email=None, phone=None):
    """
    新增用户
    """
    logger.info("save_user方法执行插入菜单----username:{} password:{} name:{} email:{} phone:{}"
                .format(username, password, name, email, phone))

    # 创建数据库连接
    conn = pool.connection()

    # 创建游标对象
    cursor = conn.cursor()
    # 生成一个随机的UUID
    random_uuid = uuid.uuid4()
    user_id = random_uuid.hex
    md5_password = gen_md5(salt + password)
    # 执行插入语句
    insert_sql = "INSERT INTO t_user (user_id, name, username, password, email, phone) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (user_id, name, username, md5_password, email, phone)
    cursor.execute(insert_sql, values)

    # 提交更改
    conn.commit()
    logger.info("save_user执行新增用户完成----user_id:{}".format(user_id))

    # 关闭游标和数据库连接
    cursor.close()
    conn.close()
    return user_id


def get_by_user_id(user_id):
    """
    通过user_id查询用户信息 user_id是uuid
    """
    # 创建数据库连接
    conn = pool.connection()

    # 创建游标对象
    cursor = conn.cursor()

    # 执行插入语句
    query_sql = "SELECT id, user_id,name,username,email,phone FROM t_user WHERE user_id=%s "
    cursor.execute(query_sql, user_id)
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


def update_user(user_id, name, email=None, phone=None):
    """
    更新用户的信息
    """
    logger.info(
        "update_user方法执行更新用户信息----user_id:{},name:{} email:{} phone:{} ".format(user_id, name, email, phone))

    # 创建数据库连接
    conn = pool.connection()

    # 创建游标对象
    cursor = conn.cursor()

    update_sql = "UPDATE t_user SET name = %s, email = %s, phone = %s WHERE user_id = %s"
    values = (name, email, phone, user_id)
    cursor.execute(update_sql, values)

    # 提交更改
    conn.commit()
    logger.info("update_user方法执行更新用户信息完成")

    # 关闭游标和数据库连接
    cursor.close()
    conn.close()


def delete_by_user_id(user_id):
    """
    通过user_id删除用户  user_id是uuid
    """
    # 创建数据库连接
    conn = pool.connection()

    # 创建游标对象
    cursor = conn.cursor()

    query = "DELETE FROM t_user WHERE user_id = %s"
    cursor.execute(query, user_id)

    # 提交更改
    conn.commit()

    # 关闭游标和数据库连接
    cursor.close()
    conn.close()
