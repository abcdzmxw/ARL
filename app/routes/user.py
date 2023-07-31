import uuid

from flask import request
from flask_restx import fields, Namespace
from app.utils import get_logger, auth
from app import utils
from . import ARLResource, get_arl_parser
from ..modules import ErrorMsg
from ..services.system.captcha_service import generate_verification_validate_code, generate_verification_image
from ..services.system.redis_service import get_redis_utils
from ..services.system.role_service import get_by_role_id, delete_user_role, save_user_role
from ..services.system.user_service import user_page_list, is_exist_user, save_user, get_by_user_id, update_user, \
    delete_by_user_id
from ..utils.user import reset_password

redis_utils = get_redis_utils()
ns = Namespace('user', description="管理员登录认证")

logger = get_logger()

login_fields2 = ns.model('LoginARL', {
    'username': fields.String(required=True, description="用户名"),
    'password': fields.String(required=True, description="密码"),
    'validate_code': fields.String(required=True, description="验证码"),
    'user_key': fields.String(required=True, description="验证码标识")
})

login_fields = ns.model('LoginARL2', {
    'username': fields.String(required=True, description="用户名"),
    'password': fields.String(required=True, description="密码")
})


@ns.route('/login')
class LoginARL(ARLResource):

    @ns.expect(login_fields)
    def post(self):
        """
        用户登录(不要验证码)
        """
        args = self.parse_args(login_fields)
        data = utils.user_login(**args)
        return utils.build_ret(ErrorMsg.Success, data)


@ns.route('/login2')
class LoginARL2(ARLResource):

    @ns.expect(login_fields2)
    def post(self):
        """
        用户登录(要验证码)
        """
        args = self.parse_args(login_fields2)
        data = utils.user_login2(**args)
        return utils.build_ret(ErrorMsg.Success, data)


@ns.route('/logout')
class LogoutARL(ARLResource):

    @auth
    def get(self):
        """
        用户退出
        """
        utils.user_logout()
        ret = {
            "message": "退出成功!",
            "code": 200,
            "data": {}
        }
        return ret


change_pass_fields = ns.model('ChangePassARL', {
    'old_password': fields.String(required=True, description="旧密码"),
    'new_password': fields.String(required=True, description="新密码"),
    'check_password': fields.String(required=True, description="确认密码"),
})


@ns.route('/change_pass')
class ChangePassARL(ARLResource):

    @auth
    @ns.expect(change_pass_fields)
    def post(self):
        """
        用户修改自己的密码
        """
        args = self.parse_args(change_pass_fields)
        ret = {
            "message": "success",
            "code": 200,
            "data": {}
        }
        token = request.headers.get("token")

        if args["new_password"] != args["check_password"]:
            ret["code"] = 301
            ret["message"] = "新密码和确定密码不一致"
            return ret

        if not args["new_password"]:
            ret["code"] = 302
            ret["message"] = "新密码不能为空"
            return ret

        if utils.change_pass(token, args["old_password"], args["new_password"]):
            utils.user_logout()
        else:
            ret["message"] = "旧密码错误"
            ret["code"] = 303

        return ret


search_user_fields = ns.model('SearchUser', {
    'page': fields.Integer(required=True, description="当前页数"),
    'size': fields.Integer(required=True, description="每页条数"),
    'username': fields.String(required=False, description="账号"),
    'name': fields.String(required=False, description="用户名称"),
    'phone': fields.String(required=False, description="电话"),
    'email': fields.String(required=False, description="邮箱")
})


@ns.route('/pageList')
class MenuPageList(ARLResource):
    parser = get_arl_parser(search_user_fields, location='args')

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
        return utils.return_msg(code=200, message="success", data=data)


add_user_fields = ns.model('AddUser', {
    'username': fields.String(required=True, description="账户"),
    'password': fields.String(required=True, description="密码"),
    'name': fields.String(required=True, description="用户名称"),
    'email': fields.String(required=False, description="邮箱"),
    'phone': fields.String(required=False, description="电话")
})

update_user_fields = ns.model('updateUser', {
    'user_id': fields.String(required=True, description="用户id"),
    'name': fields.String(required=True, description="用户名称"),
    'email': fields.String(required=False, description="邮箱"),
    'phone': fields.String(required=False, description="电话")
})

delete_user_fields = ns.model('deleteUser', {
    'user_id': fields.String(required=True, description="用户id")
})


@ns.route('/')
class ARLUser(ARLResource):

    @auth
    @ns.expect(add_user_fields)
    def post(self):
        """
        管理员添加用户
        """
        args = self.parse_args(add_user_fields)

        username = args.pop('username')
        password = args.pop('password')
        name = args.pop('name')
        email = args.pop('email', None)
        phone = args.pop('phone', None)
        try:
            # 判断是否存在记录
            count = is_exist_user(username)
            if count > 0:
                return utils.return_msg(code=500, message="此账户已经存在了", data=None)
            save_user(username=username, password=password, name=name, email=email, phone=phone)
            logger.info("新增用户完成----")
        except Exception as e:
            logger.exception(e)
            return utils.build_ret(ErrorMsg.Error, {"error": str(e)})

        """这里直接返回成功了"""
        return utils.return_msg(code=200, message="新增成功")

    @auth
    @ns.expect(update_user_fields)
    def patch(self):
        """
        管理员修改用户信息
        """
        args = self.parse_args(update_user_fields)
        user_id = args.pop('user_id')
        name = args.pop('name')
        email = args.pop('email', None)
        phone = args.pop('phone', None)

        logger.info("执行插入菜单入参：user_id:{} name:{} email:{} phone:{}".format(user_id, name, email, phone))

        try:
            # 判断是否存在记录
            arl_user = get_by_user_id(user_id=user_id)
            if arl_user is None:
                return utils.return_msg(code=500, message="用户不存在", data=None)
            update_user(user_id=user_id, name=name, email=email, phone=phone)
        except Exception as e:
            logger.exception(e)
            return utils.build_ret(ErrorMsg.Error, {"error": str(e)})

        """这里直接返回成功了"""
        return utils.return_msg(code=200, message="修改成功")

    @auth
    @ns.expect(delete_user_fields)
    def delete(self):
        """
        管理员删除用户
        """
        args = self.parse_args(delete_user_fields)
        user_id = args.pop('user_id')
        try:
            userObj = get_by_user_id(user_id=user_id)
            delete_by_user_id(user_id=user_id)

            # 删除该用户的角色对应关系信息
            if userObj:
                delete_user_role(user_id=userObj['id'])

        except Exception as e:
            logger.exception(e)
            return utils.build_ret(ErrorMsg.Error, {"error": str(e)})

        """这里直接返回成功了"""
        return utils.return_msg(code=200, message="删除成功")


@ns.route('/<string:user_id>')
class DetailUser(ARLResource):
    @auth
    def get(self, user_id=None):
        """
        通过用户id查询用户详情
        """
        logger.info("user_id.....{}".format(user_id))
        arl_user = get_by_user_id(user_id=user_id)
        if arl_user is None:
            return utils.return_msg(code=500, message="用户不存在", data=None)

        return utils.return_msg(code=200, message="success", data=arl_user)


assign_user_role_fields = ns.model('assignRole', {
    'role_id': fields.String(required=True, description="角色id")
})


@ns.route('/assignRole/<string:user_id>')
class UserAssignRole(ARLResource):
    @auth
    @ns.expect(assign_user_role_fields)
    def patch(self, user_id=None):
        """
        管理员给用户分配角色
        """

        arl_user = get_by_user_id(user_id=user_id)
        if arl_user is None:
            return utils.return_msg(code=500, message="用户不存在", data=None)

        args = self.parse_args(assign_user_role_fields)
        role_id_str = args.pop('role_id')
        logger.info("user_id.....{}, role_id_str={}".format(user_id, role_id_str))
        role_id_array = role_id_str.split(',')

        logger.info("user_id.....{}, role_id_str={},role_id_array={}".format(user_id, role_id_str, role_id_array))
        for role_id in role_id_array:
            logger.info("role_id.....{}".format(role_id))
            role = get_by_role_id(role_id=role_id)
            if role is None:
                return utils.return_msg(code=500, message="选择了不存在的角色", data=None)

        logger.info("删除已分配的角色:{}", arl_user)
        delete_user_role(arl_user['id'])
        logger.info("开始执行保存.....arl_user:{}", arl_user)
        save_user_role(user_id=arl_user['id'], role_id_str=role_id_str)

        return utils.return_msg(code=200, message="分配成功")


reset_pass_fields = ns.model('ResetPassARL', {
    'password': fields.String(required=True, description="密码"),
    'user_id': fields.String(required=True, description="用户id")
})


@ns.route('/reset_password')
class ResetPassARL(ARLResource):

    @auth
    @ns.expect(reset_pass_fields)
    def post(self):
        """
        管理员给用户重置密码
        """
        args = self.parse_args(reset_pass_fields)
        user_id = args.pop('user_id')
        password = args.pop('password')
        arl_user = get_by_user_id(user_id=user_id)
        if arl_user is None:
            return utils.return_msg(code=500, message="用户不存在", data=None)

        reset_password(user_id=user_id, password=password)
        return utils.return_msg(code=200, message="密码重置成功!")


@ns.route('/captcha')
class CaptchaARL(ARLResource):

    def get(self):
        """
        获取验证码
        """
        logger.info("开始获取验证码..................")
        # 生成验证码
        validate_code = generate_verification_validate_code()
        # 生成验证码图片
        encoded_image = generate_verification_image(validate_code=validate_code)

        random_uuid = uuid.uuid4()
        user_key = random_uuid.hex

        # 设置键为'key'，值为'value'，过期时间为2分钟=120秒
        redis_utils.set(key=user_key, value=validate_code, expiration=120)

        obj = {"userKey": user_key, "captcherImg": encoded_image}

        return utils.build_ret(ErrorMsg.Success, obj)
