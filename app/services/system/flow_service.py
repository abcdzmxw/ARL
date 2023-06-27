from flask import g

from app import utils
from app.services.system.db_utils import get_db_utils

db_utils = get_db_utils()
logger = utils.get_logger()


def save_flow(title, domain, flaw_data_package, flaw_detail_data):
    created_by = g.get('current_user')
    insert_sql = "INSERT INTO t_arl_flaw (title, domain, flaw_data_package, flaw_detail_data, status, created_by) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (title, domain, flaw_data_package, flaw_detail_data, 0, created_by)
    logger.info("save_flow, insert_sql={}, values={}".format(insert_sql, values))
    db_utils.execute_insert(sql=insert_sql, args=values)
    logger.info("save_menu执行插入菜单完成----")


def get_by_id(flow_id):
    # 执行查询语句
    query_sql = "SELECT t.id,t.title,t.domain,t.flaw_data_package,t.flaw_detail_data,t.`status`,DATE_FORMAT(t.submit_time, '%Y-%m-%d %H:%i:%s') as submit_time,DATE_FORMAT(t.process_time, '%Y-%m-%d %H:%i:%s') as process_time,t.process_by,DATE_FORMAT(t.created_at, '%Y-%m-%d %H:%i:%s') as created_at,t.created_by FROM t_arl_flaw t WHERE t.id= "
    query_sql += str(flow_id)
    logger.info("get_by_id, query_sql={}".format(query_sql))
    flow_obj = db_utils.get_one(sql=query_sql)
    return flow_obj


def flow_page_list(args):
    page = args.pop("page", 1)
    size = args.pop("size", 10)
    title = args.pop("title")
    domain = args.pop("domain")
    status = args.pop("status")

    # 执行分页查询
    query_sql = "SELECT t.id,t.title,t.domain,t.flaw_data_package,t.flaw_detail_data,t.`status`,DATE_FORMAT(t.submit_time, '%Y-%m-%d %H:%i:%s') as submit_time,DATE_FORMAT(t.process_time, '%Y-%m-%d %H:%i:%s') as process_time,t.process_by,DATE_FORMAT(t.created_at, '%Y-%m-%d %H:%i:%s') as created_at,t.created_by FROM t_arl_flaw t WHERE 1=1"

    condition = " AND created_by='{}'".format(g.get('current_user'))
    # 如果条件存在，则添加条件到查询语句
    if title:
        condition += " AND title LIKE '%{}%'".format(title)

    if domain:
        condition += " AND domain LIKE '%{}%'".format(domain)

    if status:
        condition += " AND status='{}'".format(status)

    count_query_sql = "SELECT count(*) FROM t_arl_flaw t WHERE 1=1 " + condition

    # 计算查询的起始位置
    offset = (page - 1) * size
    limit_info = " LIMIT " + str(size) + " OFFSET " + str(offset)
    query_sql = query_sql + condition + limit_info

    logger.info("flow_page_list, query_sql={},count_query_sql={}".format(query_sql, count_query_sql))
    query_total = db_utils.get_query_total(sql=count_query_sql)
    menu_list = db_utils.get_query_list(sql=query_sql)

    result = {
        "page": page,
        "size": size,
        "total": query_total,
        "items": menu_list
    }

    return result


def admin_flow_page_list(args):
    page = args.pop("page", 1)
    size = args.pop("size", 10)
    title = args.pop("title")
    domain = args.pop("domain")
    status = args.pop("status")

    # 执行分页查询
    query_sql = "SELECT t.id,t.title,t.domain,t.flaw_data_package,t.flaw_detail_data,t.`status`,DATE_FORMAT(t.submit_time, '%Y-%m-%d %H:%i:%s') as submit_time,DATE_FORMAT(t.process_time, '%Y-%m-%d %H:%i:%s') as process_time,t.process_by,DATE_FORMAT(t.created_at, '%Y-%m-%d %H:%i:%s') as created_at,t.created_by FROM t_arl_flaw t WHERE 1=1"

    condition = ""
    # 如果条件存在，则添加条件到查询语句
    if title:
        condition += " AND title LIKE '%{}%'".format(title)

    if domain:
        condition += " AND domain LIKE '%{}%'".format(domain)

    condition += " AND status in({},{},{})".format('1', '2', '3')

    count_query_sql = "SELECT count(*) FROM t_arl_flaw t WHERE 1=1 " + condition

    # 计算查询的起始位置
    offset = (page - 1) * size
    limit_info = " LIMIT " + str(size) + " OFFSET " + str(offset)
    query_sql = query_sql + condition + limit_info
    logger.info("admin_flow_page_list, query_sql={},count_query_sql={}".format(query_sql, count_query_sql))
    query_total = db_utils.get_query_total(sql=count_query_sql)
    menu_list = db_utils.get_query_list(sql=query_sql)

    result = {
        "page": page,
        "size": size,
        "total": query_total,
        "items": menu_list
    }

    return result


def submit_flow(flow_id, status):
    created_by = g.get('current_user')
    update_sql = "UPDATE t_arl_flaw SET status = %s, updated_at=NOW(), updated_by = %s, submit_time = now() WHERE id = %s"
    values = (status, created_by, flow_id)
    logger.info("submit_flow, update_sql={},values={}".format(update_sql, values))
    db_utils.execute_update(sql=update_sql, args=values)


def process_flow(flow_id, status):
    update_sql = "UPDATE t_arl_flaw SET status = %s, process_time=now(),process_by= %s WHERE id= %s"
    username = g.get('current_user')
    values = (status, username, flow_id)
    logger.info("process_flow, update_sql={},values={}".format(update_sql, values))
    db_utils.execute_update(sql=update_sql, args=values)
