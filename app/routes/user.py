from flask import request
from flask_restx import fields, Namespace
from app.utils import get_logger, auth
from app import utils
from . import ARLResource, get_arl_parser
from app import modules
from ..modules import ErrorMsg
from ..services.system.user_service import user_page_list

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
