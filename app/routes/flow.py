import datetime
from flask_restx import fields, Namespace
from app.utils import get_logger, auth, return_msg
from . import ARLResource, get_arl_parser
from app import utils
from app.modules import ErrorMsg
from ..services.system.flow_service import save_flow, flow_page_list, admin_flow_page_list, get_by_id, submit_flow, \
    process_flow, update_flow, delete_by_flow_id
from flask import g

ns = Namespace('flow', description="漏洞管理")

logger = get_logger()

search_flow_fields = ns.model('SearchFlow', {
    'page': fields.Integer(required=True, description="当前页数", example=1),
    'size': fields.Integer(required=True, description="页面大小", example=10),
    'title': fields.String(required=False, description="标题"),
    'domain': fields.String(required=False, description="站点"),
    'status': fields.String(required=False, description="状态")
})

add_flow_fields = ns.model('AddFlow', {
    'title': fields.String(required=True, description="标题"),
    'domain': fields.String(required=True, description="域名"),
    'flaw_data_package': fields.String(required=True, description="漏洞数据包"),
    'flaw_detail_data': fields.String(required=True, description="漏洞详情")
})

update_flow_fields = ns.model('UpdateFlow', {
    'id': fields.Integer(required=True, description="id"),
    'title': fields.String(required=True, description="标题"),
    'domain': fields.String(required=True, description="域名"),
    'flaw_data_package': fields.String(required=True, description="漏洞数据包"),
    'flaw_detail_data': fields.String(required=True, description="漏洞详情")
})

delete_flow_fields = ns.model('deleteFlow', {
    'id': fields.Integer(required=True, description="漏洞id")
})


@ns.route('/')
class ARLFlow(ARLResource):

    @auth
    @ns.expect(add_flow_fields)
    def post(self):
        """
        添加漏洞
        """
        args = self.parse_args(add_flow_fields)

        title = args.pop('title')
        domain = args.pop('domain')
        flaw_data_package = args.pop('flaw_data_package')
        flaw_detail_data = args.pop('flaw_detail_data')

        try:
            inserted_id = save_flow(title=title, domain=domain, flaw_data_package=flaw_data_package,
                                    flaw_detail_data=flaw_detail_data)
            logger.info("执行插入菜单完成----inserted_id:{}".format(inserted_id))
        except Exception as e:
            logger.exception(e)
            return utils.build_ret(ErrorMsg.Error, {"error": str(e)})
        return return_msg(code=200, message="success")

    @auth
    @ns.expect(update_flow_fields)
    def patch(self):
        """
        修改漏洞
        """
        args = self.parse_args(update_flow_fields)
        flow_id = args.pop('id')
        title = args.pop('title')
        domain = args.pop('domain')
        flaw_data_package = args.pop('flaw_data_package')
        flaw_detail_data = args.pop('flaw_detail_data')

        try:
            flow = get_by_id(flow_id)
            if flow is None:
                return utils.return_msg(code=500, message="该漏洞不存在", data=None)
            else:
                if flow['status'] == '1' or flow['status'] == '2':
                    return utils.return_msg(code=500, message="漏洞目前状态不允许修改", data=None)

            update_flow(flow_id=flow_id, title=title, domain=domain, flaw_data_package=flaw_data_package,
                        flaw_detail_data=flaw_detail_data)

        except Exception as e:
            logger.exception(e)
            return utils.build_ret(ErrorMsg.Error, {"error": str(e)})

        return return_msg(code=200, message="success")

    @auth
    @ns.expect(delete_flow_fields)
    def delete(self):
        """
        删除漏洞
        """
        args = self.parse_args(delete_flow_fields)
        flow_id = args.pop('id')
        try:
            flow = get_by_id(flow_id)
            if flow is None:
                return utils.return_msg(code=500, message="该漏洞不存在", data=None)
            else:
                if flow['status'] != '0':
                    return utils.return_msg(code=500, message="漏洞目前状态不允许删除", data=None)

            delete_by_flow_id(flow_id=flow_id)
        except Exception as e:
            logger.exception(e)
            return utils.build_ret(ErrorMsg.Error, {"error": str(e)})

        """这里直接返回成功了"""
        return utils.return_msg(code=200, message="删除成功")


@ns.route('/pageList')
class FlowPageList(ARLResource):
    parser = get_arl_parser(search_flow_fields, location='args')

    @auth
    @ns.expect(parser)
    def get(self):
        """
        查询自己创建的漏洞列表
        """
        args = self.parser.parse_args()
        try:
            data = flow_page_list(args=args)
            logger.info("数据已经返回111.....{}".format(data))
            return return_msg(code=200, message="success", data=data)
        except Exception as e:
            logger.exception(e)
            return utils.build_ret(ErrorMsg.Error, {"error": str(e)})


@ns.route('/get_status')
class DomainBruteTypeTask(ARLResource):
    @auth
    def get(self):
        """
        获取漏洞状态-字典
        """
        data = [
            {"key": "0", "value": "待提交"},
            {"key": "1", "value": "待审核"},
            {"key": "2", "value": "审核通过"},
            {"key": "3", "value": "审核不通过"}
        ]

        return utils.return_msg(200, "漏洞状态", data)


@ns.route('/admin/pageList')
class AdminFlowPageList(ARLResource):
    parser = get_arl_parser(search_flow_fields, location='args')

    @auth
    @ns.expect(parser)
    def get(self):
        """
        管理员查询待审核+已经处理的漏洞列表
        """
        args = self.parser.parse_args()
        try:
            data = admin_flow_page_list(args=args)
            logger.info("数据已经返回111.....{}".format(data))
        except Exception as e:
            logger.exception(e)
            return utils.build_ret(ErrorMsg.Error, {"error": str(e)})

        """这里直接返回成功了"""
        return utils.build_ret(ErrorMsg.Success, data)


@ns.route('/<int:flow_id>')
class DetailFlow(ARLResource):
    @auth
    def get(self, flow_id=None):
        """
        根据id查询漏洞详情
        """
        logger.info("DetailFlow,flow_id={}".format(flow_id))
        data = get_by_id(flow_id=flow_id)
        logger.info("数据已经返回111.....{}".format(data))
        return utils.build_ret(ErrorMsg.Success, data)


submit_flow_fields = ns.model('submitFlow', {
    'status': fields.String(required=True, description="状态")
})


@ns.route('/submit/<int:flow_id>')
class SubmitFlow(ARLResource):
    @auth
    @ns.expect(submit_flow_fields)
    def patch(self, flow_id=None):
        """
        提交或者撤回操作
        """
        args = self.parse_args(submit_flow_fields)

        status = args.pop('status')

        flow_obj = get_by_id(flow_id=flow_id)
        if flow_obj is None:
            return return_msg(code=5000, message="此漏洞被删除了,无法操作")

        username = g.get('current_user')
        if flow_obj['created_by'] != username:
            return return_msg(code=5000, message="创建人才能操作该记录")

        if status == "1":
            if flow_obj['status'] != "0":
                return return_msg(code=5000, message="操作已过期,请刷新后再操作")
        else:
            if status == "0":
                if flow_obj['status'] != "1":
                    return return_msg(code=5000, message="已提交(待审核)的数据才允许撤回")
            else:
                return return_msg(code=5000, message="请求的状态不对,无法操作")

        submit_flow(flow_id=flow_id, status=status)

        return return_msg(code=200, message="操作成功!")


@ns.route('/process/<int:flow_id>')
class ProcessFlow(ARLResource):
    @auth
    @ns.expect(submit_flow_fields)
    def patch(self, flow_id=None):
        """
        审核处理操作
        """
        args = self.parse_args(submit_flow_fields)

        status = args.pop('status')

        flow_obj = get_by_id(flow_id=flow_id)
        if flow_obj is None:
            return return_msg(code=5000, message="此漏洞被删除了,无法操作")

        if status == "2" or status == "3":
            if flow_obj['status'] != "1":
                return return_msg(code=5000, message="操作已过期,请刷新后再操作")
        else:
            return return_msg(code=5000, message="请求的状态不对,无法操作")

        process_flow(flow_id=flow_id, status=status)

        return return_msg(code=200, message="操作成功!")
