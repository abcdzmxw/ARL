from flask_restx import fields, Namespace
from app.utils import get_logger, auth
from . import ARLResource, get_arl_parser
from app import utils
from app.modules import ErrorMsg
from flask import g

from ..services.system.menu_service import delete_role_menu_by_role_id
from ..services.system.role_service import get_by_role_code, save_role, get_by_role_id, update_role, delete_by_role_id, \
    role_page_list, get_user_role_list, role_list, user_use_role, get_user_role_list_by_userid

ns = Namespace('role', description="角色管理")

logger = get_logger()


search_role_fields = ns.model('SearchRole', {
    'page': fields.Integer(required=True, description="当前页数"),
    'size': fields.Integer(required=True, description="每页条数"),
    'role_name': fields.String(required=False, description="角色名称"),
    'role_code': fields.String(required=False, description="角色编码")
})

add_role_fields = ns.model('AddRole', {
    'role_name': fields.String(required=True, description="角色名称"),
    'role_code': fields.String(required=True, description="角色编码")
})

update_role_fields = ns.model('updateRole', {
    'id': fields.Integer(required=True, description="角色id"),
    'role_name': fields.String(required=True, description="角色名称"),
    'role_code': fields.String(required=True, description="角色编码")
})

delete_role_fields = ns.model('deleteRole', {
    'id': fields.Integer(required=True, description="角色id")
})

user_role_fields = ns.model('getUserRole', {
    'user_id': fields.String(required=True, description="用户id")
})


@ns.route('/')
class ARLRole(ARLResource):

    @auth
    @ns.expect(add_role_fields)
    def post(self):
        """
        新增角色
        """
        args = self.parse_args(add_role_fields)

        role_name = args.pop('role_name')
        role_code = args.pop('role_code')

        # 判断是否存在记录
        role = get_by_role_code(role_code)
        if role:
            return utils.return_msg(code=500, message="此角色已经存在了", data=None)

        try:
            save_role(role_name=role_name, role_code=role_code)
        except Exception as e:
            logger.exception(e)
            return utils.build_ret(ErrorMsg.Error, {"error": str(e)})

        """这里直接返回成功了"""
        return utils.return_msg(code=200, message="新增角色成功")

    @auth
    @ns.expect(update_role_fields)
    def patch(self):
        """
        修改角色
        """
        args = self.parse_args(update_role_fields)
        role_name = args.pop('role_name')
        role_code = args.pop('role_code')
        role_id = args.pop('id')
        # 判断是否存在记录
        role = get_by_role_id(role_id=role_id)
        if role is None:
            return utils.return_msg(code=500, message="角色不存在", data=None)

        roleObj = get_by_role_code(role_code=role_code)

        if roleObj is not None:
            if role['id'] != roleObj['id']:
                return utils.return_msg(code=500, message="角色编码已经存在,请更换一个", data=None)

        try:
            update_role(role_id=role_id, role_name=role_name)
        except Exception as e:
            logger.exception(e)
            return utils.build_ret(ErrorMsg.Error, {"error": str(e)})

        """这里直接返回成功了"""
        return utils.return_msg(code=200, message="修改角色成功")

    @auth
    @ns.expect(delete_role_fields)
    def delete(self):
        """
        删除角色
        """
        args = self.parse_args(delete_role_fields)
        role_id = args.pop('id')
        try:
            count = user_use_role(role_id=role_id)
            if count > 0:
                return utils.return_msg(code=500, message="角色已被用户用户引用,请取消引用后再删除角色!", data=None)

            # 删除角色
            delete_by_role_id(role_id=role_id)

            # 删除角色菜单对应关系信息
            delete_role_menu_by_role_id(role_id=role_id)
        except Exception as e:
            logger.exception(e)
            return utils.build_ret(ErrorMsg.Error, {"error": str(e)})

        """这里直接返回成功了"""
        return utils.return_msg(code=200, message="删除成功")


@ns.route('/pageList')
class MenuPageList(ARLResource):
    parser = get_arl_parser(search_role_fields, location='args')

    @auth
    @ns.expect(parser)
    def get(self):
        """
        查询角色列表
        """
        args = self.parser.parse_args()
        try:
            data = role_page_list(args=args)
            logger.info("数据已经返回111.....{}".format(data))
        except Exception as e:
            logger.exception(e)
            return utils.build_ret(ErrorMsg.Error, {"error": str(e)})

        logger.info("数据已经返回222.....{}".format(data))
        """这里直接返回成功了"""
        return utils.build_ret(ErrorMsg.Success, data)


@ns.route('/assignRoleList')
class AssignRoleList(ARLResource):
    @auth
    def get(self):
        """
        查询当前用户角色列表
        """
        current_user = g.get('current_user')
        logger.info("current_user.....{}".format(current_user))

        data = get_user_role_list(username=current_user)
        return utils.build_ret(ErrorMsg.Success, data)


@ns.route('/getUserRoleList')
class UserRoleList(ARLResource):
    parser = get_arl_parser(user_role_fields, location='args')

    @auth
    @ns.expect(parser)
    def get(self):
        """
        查询用户角色列表
        """
        args = self.parser.parse_args()
        user_id = args.pop("user_id")
        logger.info("user_id.....{}".format(user_id))
        data = get_user_role_list_by_userid(user_id=user_id)
        return utils.build_ret(ErrorMsg.Success, data)


@ns.route('/list')
class MenuList(ARLResource):

    @auth
    @ns.expect()
    def get(self):
        """
        查询所有角色列表
        """
        try:
            data = role_list()
            logger.info("数据已经返回111.....{}".format(data))
        except Exception as e:
            logger.exception(e)
            return utils.build_ret(ErrorMsg.Error, {"error": str(e)})
        return utils.build_ret(ErrorMsg.Success, data)
