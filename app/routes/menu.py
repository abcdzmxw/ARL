from flask_restx import Resource, Api, reqparse, fields, Namespace
from bson import ObjectId
from app import celerytask
from app.utils import get_logger, auth
from . import base_query_fields, ARLResource, get_arl_parser, conn
from app import utils
from app.modules import TaskStatus, ErrorMsg, TaskSyncStatus, CeleryAction, TaskTag, TaskType
from app.helpers import get_options_by_policy_id, submit_task_task, \
    submit_risk_cruising, get_scope_by_scope_id, check_target_in_scope
from app.helpers.task import get_task_data, restart_task
from ..services.system.menu_service import save_menu, menu_page_list, is_exist_menu_code, get_by_id, update_menu, \
    delete_menu_by_id, get_menu_by_role_id, get_user_menu_list, get_first_level_menu_list
from flask import g

ns = Namespace('menu', description="菜单管理")

logger = get_logger()

base_search_task_fields = {
    'menu_name': fields.String(required=False, description="菜单名称"),
    'menu_code': fields.String(required=False, description="菜单编码"),
    'route': fields.String(required=False, description="前端路由编码")
}

base_search_task_fields.update(base_query_fields)

search_task_fields = ns.model('SearchTask', base_search_task_fields)

add_task_fields = ns.model('AddTask', {
    'name': fields.String(required=True, description="任务名"),
    'target': fields.String(required=True, description="目标"),
    "domain_brute": fields.Boolean(),
    'domain_brute_type': fields.String(),
    "port_scan_type": fields.String(description="端口扫描类型"),
    "port_scan": fields.Boolean(),
    "service_detection": fields.Boolean(),
    "service_brute": fields.Boolean(example=False),
    "os_detection": fields.Boolean(example=False),
    "site_identify": fields.Boolean(example=False),
    "site_capture": fields.Boolean(example=False),
    "file_leak": fields.Boolean(example=False),
    "search_engines": fields.Boolean(example=False),
    "site_spider": fields.Boolean(example=False),
    "arl_search": fields.Boolean(example=False),
    "alt_dns": fields.Boolean(),
    "github_search_domain": fields.Boolean(),
    "ssl_cert": fields.Boolean(),
    "fetch_api_path": fields.Boolean(),
    "dns_query_plugin": fields.Boolean(example=False, default=False),
    "skip_scan_cdn_ip": fields.Boolean(),
    "nuclei_scan": fields.Boolean(description="nuclei 扫描", example=False, default=False),
    "findvhost": fields.Boolean()
})

add_menu_fields = ns.model('AddMenu', {
    'menu_name': fields.String(required=True, description="菜单名称"),
    'menu_code': fields.String(required=True, description="菜单编码"),
    'sort': fields.String(required=True, description="排序"),
    'parent_id': fields.String(required=False, description="父菜单id"),
    'click_uri': fields.String(required=False, description="uri"),
    'route': fields.String(required=False, description="前端路由编码")
})

update_menu_fields = ns.model('updateMenu', {
    'menu_id': fields.String(required=True, description="菜单id"),
    'menu_name': fields.String(required=True, description="菜单名称"),
    'sort': fields.String(required=True, description="排序"),
    'parent_id': fields.String(required=False, description="父菜单id"),
    'click_uri': fields.String(required=False, description="uri"),
    'route': fields.String(required=False, description="前端路由编码")
})

delete_menu_fields = ns.model('deleteMenu', {
    'menu_id': fields.String(required=True, description="菜单id")
})


@ns.route('/')
class ARLTask(ARLResource):

    @auth
    @ns.expect(add_menu_fields)
    def post(self):
        """
        添加菜单
        """
        args = self.parse_args(add_menu_fields)

        menu_name = args.pop('menu_name')
        menu_code = args.pop('menu_code')
        sort = args.pop('sort')
        parent_id = args.pop('parent_id', None)
        click_uri = args.pop('click_uri', None)
        route = args.pop('route', None)
        logger.info("执行插入菜单入参：menu_name:{} menu_code:{} sort:{} parent_id:{} click_uri:{} route:{}"
                    .format(menu_name, menu_code, sort, parent_id, click_uri, route))
        # 判断是否存在记录
        count = is_exist_menu_code(menu_code)
        if count > 0:
            return utils.return_msg(code=500, massage="此编码已经存在了", data=None)

        # 父菜单传了的话，校验此菜单id是否存在
        logger.info("通过菜单id查询菜单----parent_id:{}".format(parent_id))
        if parent_id is not None:
            menu = get_by_id(menu_id=parent_id)
            logger.info("通过菜单id查询菜单----parent_id{},menu:{}".format(parent_id, menu))
            if menu is None:
                return utils.return_msg(code=500, massage="父菜单不存在", data=None)

        try:
            inserted_id = save_menu(menu_name=menu_name, menu_code=menu_code, sort=sort, parent_id=parent_id,
                                    click_uri=click_uri, route=route)
            logger.info("执行插入菜单完成----inserted_id:{}".format(inserted_id))
        except Exception as e:
            logger.exception(e)
            return utils.build_ret(ErrorMsg.Error, {"error": str(e)})

        """这里直接返回成功了"""
        return utils.build_ret(ErrorMsg.Success, inserted_id)

    @auth
    @ns.expect(update_menu_fields)
    def patch(self):
        """
        修改菜单
        """
        args = self.parse_args(update_menu_fields)
        menu_id = args.pop('menu_id')
        menu_name = args.pop('menu_name')
        sort = args.pop('sort')
        parent_id = args.pop('parent_id', None)
        click_uri = args.pop('click_uri', None)
        route = args.pop('route', None)
        logger.info("执行插入菜单入参：menu_name:{} sort:{} parent_id:{} click_uri:{} route:{}"
                    .format(menu_name, sort, parent_id, click_uri, route))
        # 判断是否存在记录
        menu = get_by_id(menu_id=menu_id)
        if menu is None:
            return utils.return_msg(code=500, massage="菜单不存在", data=None)

        # 父菜单传了的话，校验此菜单id是否存在
        logger.info("通过菜单id查询菜单----parent_id:{}".format(parent_id))
        if parent_id is not None:
            menu = get_by_id(menu_id=parent_id)
            logger.info("通过菜单id查询菜单----parent_id{},menu:{}".format(parent_id, menu))
            if menu is None:
                return utils.return_msg(code=500, massage="父菜单不存在", data=None)

        try:
            update_menu(menu_id=menu_id, menu_name=menu_name, sort=sort, parent_id=parent_id, click_uri=click_uri,
                        route=route)
        except Exception as e:
            logger.exception(e)
            return utils.build_ret(ErrorMsg.Error, {"error": str(e)})

        """这里直接返回成功了"""
        return utils.build_ret(ErrorMsg.Success, menu_id)

    @auth
    @ns.expect(delete_menu_fields)
    def delete(self):
        """
        修改菜单
        """
        args = self.parse_args(delete_menu_fields)
        menu_id = args.pop('menu_id')
        try:
            delete_menu_by_id(menu_id=menu_id)
        except Exception as e:
            logger.exception(e)
            return utils.build_ret(ErrorMsg.Error, {"error": str(e)})

        """这里直接返回成功了"""
        return utils.return_msg(code=200, massage="删除成功")


@ns.route('/pageList')
class MenuPageList(ARLResource):
    parser = get_arl_parser(search_task_fields, location='args')

    @auth
    @ns.expect(parser)
    def get(self):
        """
        查询菜单列表
        """
        args = self.parser.parse_args()
        try:
            data = menu_page_list(args=args)
            logger.info("数据已经返回111.....{}".format(data))
        except Exception as e:
            logger.exception(e)
            return utils.build_ret(ErrorMsg.Error, {"error": str(e)})

        logger.info("数据已经返回222.....{}".format(data))
        """这里直接返回成功了"""
        return utils.build_ret(ErrorMsg.Success, data)


@ns.route('/assignMenu/<int:role_id>')
class AssignMenu(ARLResource):
    @auth
    def get(self, role_id=None):
        """
        查询该角色拥有的菜单列表
        """
        logger.info("role_id.....{}".format(role_id))
        data = get_menu_by_role_id(role_id=role_id)
        return utils.build_ret(ErrorMsg.Success, data)


@ns.route('/getUserMenuList')
class UserMenu(ARLResource):
    @auth
    def get(self):
        """
        查询用户菜单列表
        """
        current_user = g.get('current_user')
        logger.info("current_user.....{}".format(current_user))

        data = get_user_menu_list(username=current_user)
        return utils.build_ret(ErrorMsg.Success, data)


@ns.route('/getAllFirstLevelMenuList')
class FistUserMenu(ARLResource):
    @auth
    def get(self):
        """
        获取一级菜单
        """
        data = get_first_level_menu_list()
        return utils.build_ret(ErrorMsg.Success, data)
