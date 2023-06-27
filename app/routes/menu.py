from flask_restx import fields, Namespace
from app.utils import get_logger, auth
from . import ARLResource, get_arl_parser
from app import utils
from app.modules import ErrorMsg
from ..services.system.menu_service import save_menu, menu_page_list, is_exist_menu_code, get_by_id, update_menu, \
    delete_menu_by_id, get_menu_by_role_id, get_user_menu_list, get_first_level_menu_list
from flask import g

ns = Namespace('menu', description="菜单管理")

logger = get_logger()


search_task_fields = ns.model('SearchMenu', {
    'page': fields.Integer(required=True, description="当前页数"),
    'size': fields.Integer(required=True, description="页面大小"),
    'menu_name': fields.String(required=False, description="菜单名称"),
    'menu_code': fields.String(required=False, description="菜单编码"),
    'route': fields.String(required=False, description="前端路由编码")
})

add_menu_fields = ns.model('AddMenu', {
    'menu_name': fields.String(required=True, description="菜单名称"),
    'menu_code': fields.String(required=True, description="菜单编码"),
    'sort': fields.Integer(required=True, description="排序"),
    'parent_id': fields.Integer(required=False, description="父菜单id"),
    'click_uri': fields.String(required=False, description="uri"),
    'route': fields.String(required=False, description="前端路由编码")
})

update_menu_fields = ns.model('updateMenu', {
    'id': fields.Integer(required=True, description="菜单id"),
    'menu_name': fields.String(required=True, description="菜单名称"),
    'sort': fields.Integer(required=True, description="排序"),
    'parent_id': fields.Integer(required=False, description="父菜单id"),
    'click_uri': fields.String(required=False, description="uri"),
    'route': fields.String(required=False, description="前端路由编码")
})

delete_menu_fields = ns.model('deleteMenu', {
    'menu_id': fields.Integer(required=True, description="菜单id")
})


@ns.route('/')
class ARLMenu(ARLResource):

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
        try:
            # 判断是否存在记录
            count = is_exist_menu_code(menu_code)
            if count > 0:
                return utils.return_msg(code=500, message="此编码已经存在了", data=None)

            # 父菜单传了的话，校验此菜单id是否存在
            if parent_id is not None:
                menu = get_by_id(menu_id=parent_id)
                logger.info("通过菜单id查询菜单----parent_id{},menu:{}".format(parent_id, menu))
                if menu is None:
                    return utils.return_msg(code=500, message="父菜单不存在", data=None)

            save_menu(menu_name=menu_name, menu_code=menu_code, sort=sort, parent_id=parent_id, click_uri=click_uri, route=route)
            logger.info("执行插入菜单完成----")
        except Exception as e:
            logger.exception(e)
            return utils.build_ret(ErrorMsg.Error, {"error": str(e)})

        """这里直接返回成功了"""
        return utils.return_msg(code=200, message="新增成功")

    @auth
    @ns.expect(update_menu_fields)
    def patch(self):
        """
        修改菜单
        """
        args = self.parse_args(update_menu_fields)
        menu_id = args.pop('id')
        menu_name = args.pop('menu_name')
        sort = args.pop('sort')
        parent_id = args.pop('parent_id', None)
        click_uri = args.pop('click_uri', None)
        route = args.pop('route', None)
        logger.info("执行插入菜单入参：menu_name:{} sort:{} parent_id:{} click_uri:{} route:{}"
                    .format(menu_name, sort, parent_id, click_uri, route))
        try:

            # 判断是否存在记录
            menu = get_by_id(menu_id=menu_id)
            if menu is None:
                return utils.return_msg(code=500, message="菜单不存在", data=None)

            # 父菜单传了的话，校验此菜单id是否存在
            logger.info("通过菜单id查询菜单----parent_id:{}".format(parent_id))
            if parent_id is not None:
                menu = get_by_id(menu_id=parent_id)
                logger.info("通过菜单id查询菜单----parent_id{},menu:{}".format(parent_id, menu))
                if menu is None:
                    return utils.return_msg(code=500, message="父菜单不存在", data=None)
            update_menu(menu_id=menu_id, menu_name=menu_name, sort=sort, parent_id=parent_id, click_uri=click_uri,
                        route=route)
        except Exception as e:
            logger.exception(e)
            return utils.build_ret(ErrorMsg.Error, {"error": str(e)})

        """这里直接返回成功了"""
        return utils.return_msg(code=200, message="修改成功")

    @auth
    @ns.expect(delete_menu_fields)
    def delete(self):
        """
        删除菜单
        """
        args = self.parse_args(delete_menu_fields)
        menu_id = args.pop('menu_id')
        try:
            delete_menu_by_id(menu_id=menu_id)
        except Exception as e:
            logger.exception(e)
            return utils.build_ret(ErrorMsg.Error, {"error": str(e)})

        """这里直接返回成功了"""
        return utils.return_msg(code=200, message="删除成功")


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
