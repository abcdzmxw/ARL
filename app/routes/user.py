from flask import request
from flask_restx import fields, Namespace
from app.utils import get_logger, auth
from app import utils
from . import ARLResource, get_arl_parser
from app import modules
from ..modules import ErrorMsg
from ..services.system.user_service import user_page_list, is_exist_user, save_user

ns = Namespace('user', description="管理员登录认证")

logger = get_logger()

login_fields = ns.model('LoginARL', {
    'username': fields.String(required=True, description="用户名"),
    'password': fields.String(required=True, description="密码"),
})


@ns.route('/login')
class LoginARL(ARLResource):

    @ns.expect(login_fields)
    def post(self):
        """
        用户登录
        """
        args = self.parse_args(login_fields)

        return build_data(utils.user_login(**args))


@ns.route('/logout')
class LogoutARL(ARLResource):

    def get(self):
        """
        用户退出
        """
        token = request.headers.get("Token")
        utils.user_logout(token)

        return build_data({})


change_pass_fields = ns.model('ChangePassARL', {
    'old_password': fields.String(required=True, description="旧密码"),
    'new_password': fields.String(required=True, description="新密码"),
    'check_password': fields.String(required=True, description="确认密码"),
})


@ns.route('/change_pass')
class ChangePassARL(ARLResource):
    @ns.expect(change_pass_fields)
    def post(self):
        """
        密码修改
        """
        args = self.parse_args(change_pass_fields)
        ret = {
            "message": "success",
            "code": 200,
            "data": {}
        }
        token = request.headers.get("Token")

        if args["new_password"] != args["check_password"]:
            ret["code"] = 301
            ret["message"] = "新密码和确定密码不一致"
            return ret

        if not args["new_password"]:
            ret["code"] = 302
            ret["message"] = "新密码不能为空"
            return ret

        if utils.change_pass(token, args["old_password"], args["new_password"]):
            utils.user_logout(token)
        else:
            ret["message"] = "旧密码错误"
            ret["code"] = 303

        return ret


def build_data(data):
    ret = {
        "message": "success",
        "code": 200,
        "data": {}
    }

    if data:
        ret["data"] = data
    else:
        ret["code"] = 401

    return ret


base_search_user_fields = {
    'username': fields.String(required=False, description="账号"),
    'name': fields.String(required=False, description="用户名称")
}

base_search_user_fields.update(base_search_user_fields)
search_user_fields = ns.model('SearchUser', base_search_user_fields)


@ns.route('/pageList')
class MenuPageList(ARLResource):
    parser = get_arl_parser(base_search_user_fields, location='args')

    @auth
    @ns.expect(parser)
    def get(self):
        """
        查询用户列表
        """
        args = self.parser.parse_args()
        try:
            data = user_page_list(args=args)
            logger.info("数据已经返回111.....{}".format(data))
        except Exception as e:
            logger.exception(e)
            return utils.build_ret(ErrorMsg.Error, {"error": str(e)})

        logger.info("数据已经返回222.....{}".format(data))
        """这里直接返回成功了"""
        return utils.build_ret(ErrorMsg.Success, data)


add_user_fields = ns.model('AddUser', {
    'username': fields.String(required=True, description="账户"),
    'password': fields.String(required=True, description="密码"),
    'name': fields.String(required=True, description="用户名称"),
    'email': fields.String(required=False, description="邮箱"),
    'phone': fields.String(required=False, description="电话")
})

update_user_fields = ns.model('updateUser', {
    'menu_id': fields.String(required=True, description="菜单id"),
    'menu_name': fields.String(required=True, description="菜单名称"),
    'sort': fields.String(required=True, description="排序"),
    'parent_id': fields.String(required=False, description="父菜单id"),
    'click_uri': fields.String(required=False, description="uri"),
    'route': fields.String(required=False, description="前端路由编码")
})

delete_user_fields = ns.model('deleteUser', {
    'menu_id': fields.String(required=True, description="菜单id")
})


@ns.route('/')
class ARLUser(ARLResource):

    @auth
    @ns.expect(add_user_fields)
    def post(self):
        """
        添加用户
        """
        args = self.parse_args(add_user_fields)

        username = args.pop('username')
        password = args.pop('password')
        name = args.pop('name')
        email = args.pop('email', None)
        phone = args.pop('phone', None)

        # 判断是否存在记录
        count = is_exist_user(username)
        if count > 0:
            return utils.return_msg(code=500, massage="此账户已经存在了", data=None)

        try:
            inserted_id = save_user(username=username, password=password, name=name, email=email, phone=phone)
            logger.info("新增用户完成----inserted_id:{}".format(inserted_id))
        except Exception as e:
            logger.exception(e)
            return utils.build_ret(ErrorMsg.Error, {"error": str(e)})

        """这里直接返回成功了"""
        return utils.build_ret(ErrorMsg.Success, inserted_id)
