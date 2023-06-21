import uuid

from flask import request
from flask_restx import fields, Namespace
from app.utils import get_logger, auth
from app import utils
from . import ARLResource, get_arl_parser
from ..modules import ErrorMsg
from ..services.system.captcha_service import generate_verification_validate_code, generate_verification_image
from ..services.system.redis_service import redis_utils
from ..services.system.role_service import get_by_role_id, delete_user_role, save_user_role
from ..services.system.user_service import user_page_list, is_exist_user, save_user, get_by_user_id, update_user, \
    delete_by_user_id
from ..utils.user import reset_password

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

    @auth
    @ns.expect(update_user_fields)
    def patch(self):
        """
        修改用户
        """
        args = self.parse_args(update_user_fields)
        user_id = args.pop('user_id')
        name = args.pop('name')
        email = args.pop('email', None)
        phone = args.pop('phone', None)

        logger.info("执行插入菜单入参：user_id:{} name:{} email:{} phone:{}".format(user_id, name, email, phone))
        # 判断是否存在记录
        arl_user = get_by_user_id(user_id=user_id)
        if arl_user is None:
            return utils.return_msg(code=500, massage="用户不存在", data=None)

        try:
            update_user(user_id=user_id, name=name, email=email, phone=phone)
        except Exception as e:
            logger.exception(e)
            return utils.build_ret(ErrorMsg.Error, {"error": str(e)})

        """这里直接返回成功了"""
        return utils.build_ret(ErrorMsg.Success, user_id)

    @auth
    @ns.expect(delete_user_fields)
    def delete(self):
        """
        删除用户
        """
        args = self.parse_args(delete_user_fields)
        user_id = args.pop('user_id')
        try:
            delete_by_user_id(user_id=user_id)
        except Exception as e:
            logger.exception(e)
            return utils.build_ret(ErrorMsg.Error, {"error": str(e)})

        """这里直接返回成功了"""
        return utils.return_msg(code=200, massage="删除成功")


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
            return utils.return_msg(code=500, massage="用户不存在", data=None)

        return utils.build_ret(ErrorMsg.Success, arl_user)


assign_user_role_fields = ns.model('assignRole', {
    'role_id': fields.String(required=True, description="角色id")
})


@ns.route('/assignRole/<string:user_id>')
class UserAssignRole(ARLResource):
    @auth
    @ns.expect(assign_user_role_fields)
    def patch(self, user_id=None):
        """
        给用户分配角色
        """

        arl_user = get_by_user_id(user_id=user_id)
        if arl_user is None:
            return utils.return_msg(code=500, massage="用户不存在", data=None)

        args = self.parse_args(assign_user_role_fields)
        role_id_str = args.pop('role_id')
        logger.info("user_id.....{}, role_id_str={}".format(user_id, role_id_str))
        role_id_array = role_id_str.split(',')

        logger.info("user_id.....{}, role_id_str={},role_id_array={}".format(user_id, role_id_str, role_id_array))
        for role_id in role_id_array:
            logger.info("role_id.....{}".format(role_id))
            role = get_by_role_id(role_id=role_id)
            if role is None:
                return utils.return_msg(code=500, massage="选择了不存在的角色", data=None)

        logger.info("删除已分配的角色:{}", arl_user)
        delete_user_role(arl_user['id'])
        logger.info("开始执行保存.....arl_user:{}", arl_user)
        save_user_role(user_id=arl_user['id'], role_id_str=role_id_str)

        return utils.build_ret(ErrorMsg.Success, "分配成功!")


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
        给用户重置密码
        """
        args = self.parse_args(reset_pass_fields)
        user_id = args.pop('user_id')
        password = args.pop('password')
        arl_user = get_by_user_id(user_id=user_id)
        if arl_user is None:
            return utils.return_msg(code=500, massage="用户不存在", data=None)

        reset_password(user_id=user_id, password=password)
        return utils.build_ret(ErrorMsg.Success, "密码重置成功!")


@ns.route('/captcha')
class CaptchaARL(ARLResource):

    def get(self):
        """
        获取验证码
        """
        logger.info("开始获取验证码..................")
        # 生成验证码
        validate_code = generate_verification_validate_code()
        logger.info("获取验证码..................validate_code={}", validate_code)
        # 生成验证码图片
        encoded_image = generate_verification_image(validate_code=validate_code)
        logger.info("生成的图片..................validate_code={}, encoded_image={}".format(validate_code, encoded_image))
        random_uuid = uuid.uuid4()
        user_key = random_uuid.hex

        logger.info("开始设置redi, user_key={}，validate_code={}".format(user_key, validate_code))
        # 设置键为'key'，值为'value'，过期时间为2分钟=120秒
        redis_utils.set(key=user_key, value=validate_code, expire=120)
        logger.info("设置redis完成 user_key={}，validate_code={}".format(user_key, validate_code))

        obj = {"userKey": user_key, "captcherImg": encoded_image}

        return utils.build_ret(ErrorMsg.Success, obj)
