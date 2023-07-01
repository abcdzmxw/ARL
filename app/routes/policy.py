from flask_restx import Resource, Api, reqparse, fields, Namespace
from app.utils import get_logger, auth
from . import base_query_fields, ARLResource, get_arl_parser
from app.modules import ErrorMsg
from app import utils
from bson import ObjectId

ns = Namespace('policy', description="策略信息")

logger = get_logger()

base_search_fields = {
    'name': fields.String(required=False, description="策略名称"),
    "_id": fields.String(description="策略ID")
}

base_search_fields.update(base_query_fields)


@ns.route('/get_port_scan_type')
class PortScanTypeTask(ARLResource):
    @auth
    def get(self):
        """
        获取端口扫描类型-字典
        """
        data = [
            {"key": "test", "value": "测试"},
            {"key": "top100", "value": "TOP100"},
            {"key": "top1000", "value": "TOP1000"},
            {"key": "all", "value": "全端口"},
            {"key": "custom", "value": "自定义"}
        ]

        return utils.return_msg(200, "端口扫描类型", data)


@ns.route('/get_domain_function')
class PortScanTypeTask(ARLResource):
    @auth
    def get(self):
        """
        获取域名功能列表-字典
        """
        data = [
            {"key": "domain_brute", "value": "1. 域名爆破"},
            {"key": "alt_dns", "value": "2. DNS字典智能生成"},
            {"key": "arl_search", "value": "3. ARL 历史查询"},
            {"key": "dns_query_plugin", "value": "4. 域名查询插件"},
            {"key": "port_scan", "value": "5. 端口扫描"},
            {"key": "service_detection", "value": "6. 服务识别"},
            {"key": "os_detection", "value": "7. 操作系统识别"},
            {"key": "ssl_cert", "value": "8. SSL 证书获取"},
            {"key": "skip_scan_cdn_ip", "value": "9. 跳过CDN"},
            {"key": "npoc_service_detection", "value": "10. 服务(python)识别"}
        ]

        return utils.return_msg(200, "域名功能列表", data)


@ns.route('/get_site_vuln')
class PortScanTypeTask(ARLResource):
    @auth
    def get(self):
        """
        获取站点风险功能列表-字典
        """
        data = [
            {"key": "site_identify", "value": "1. 站点识别"},
            {"key": "search_engines", "value": "2. 搜索引擎调用"},
            {"key": "site_spider", "value": "3. 站点爬虫"},
            {"key": "site_capture", "value": "4. 站点截图"},
            {"key": "file_leak", "value": "5. 文件泄露"},
            {"key": "nuclei_scan", "value": "6. nuclei 调用"}
        ]

        return utils.return_msg(200, "站点风险功能列表", data)


@ns.route('/get_poc_config')
class PortScanTypeTask(ARLResource):
    @auth
    def get(self):
        """
        获取poc配置列表-字典
        """
        data = [
            {"key": "WEB_INF_WEB_xml_leak", "value": "1. WEB-INF/web.xml 文件泄漏"},
            {"key": "Ueditor_Store_XSS", "value": "2. Ueditor 存储 XSS 漏洞"},
            {"key": "Ueditor_SSRF", "value": "3. Ueditor SSRF 漏洞"},
            {"key": "Gitlab_Username_Leak", "value": "4. Gitlab 用户名泄漏"},
            {"key": "Django_Debug_Info", "value": "5. Django 开启调试模式"},
            {"key": "ZooKeeper_noauth", "value": "6. ZooKeeper 未授权访问"},
            {"key": "Solr_noauth", "value": "7. Apache solr 未授权访问"},
            {"key": "Redis_noauth", "value": "8. Redis 未授权访问"},
            {"key": "Onlyoffice_noauth", "value": "9. Onlyoffice 未授权漏洞"},
            {"key": "Nacos_noauth", "value": "10. Nacos 未授权访问"},
            {"key": "Mongodb_noauth", "value": "11. Mongodb 未授权访问"},
            {"key": "Memcached_noauth", "value": "12. Memcached 未授权访问"},
            {"key": "Kibana_noauth", "value": "13. Kibana 未授权访问"},
            {"key": "Headless_remote_API_noauth", "value": "14. Headless Remote API 未授权访问"},
            {"key": "Hadoop_YARN_RPC_noauth", "value": "15. Hadoop YARN RCP 未授权访问漏洞"},
            {"key": "Elasticsearch_noauth", "value": "16. Elasticsearch 未授权访问"},
            {"key": "Druid_noauth", "value": "17. Druid 未授权访问"},
            {"key": "DockerRemoteAPI_noauth", "value": "18. Docker Remote API 未授权访问"},
            {"key": "Apollo_Adminservice_noauth", "value": "19. apollo-adminservice 未授权访问"},
            {"key": "Actuator_noauth_bypass_waf", "value": "20. Actuator API 未授权访问 (绕过WAF)"},
            {"key": "Actuator_noauth", "value": "21. Actuator API 未授权访问"},
            {"key": "Actuator_httptrace_noauth", "value": "22. Actuator httptrace API 未授权访问"},
            {"key": "vcenter_identify", "value": "23. 发现VMware vCenter"},
            {"key": "XXL_Job_Admin_Identify", "value": "24. 发现 xxl-job-admin"},
            {"key": "Weaver_Ecology_Identify", "value": "25. 发现泛微 Ecology"},
            {"key": "Swagger_Json_Identify", "value": "26. 发现 Swagger 文档接口"},
            {"key": "Shiro_Identify", "value": "27. 发现 Apache Shiro"},
            {"key": "Oracle_Weblogic_Console_Identify", "value": "28. 发现 Oracle Weblogic 控制台"},
            {"key": "Nacos_Identify", "value": "29. 发现 Nacos"},
            {"key": "Hystrix_Dashboard_Identify", "value": "30. 发现 Hystrix Dashboard"},
            {"key": "Harbor_Identify", "value": "31. 发现 Harbor API"},
            {"key": "Graphql_Identify", "value": "32. 发现 Graphql 接口"},
            {"key": "Grafana_Identify", "value": "33. 发现 Grafana"},
            {"key": "Finereport_Identify", "value": "34. 发现帆软 FineReport"},
            {"key": "FinereportV10_Identify", "value": "35. 发现帆软 FineReport V10"},
            {"key": "Clickhouse_REST_API_Identify", "value": "36. 发现 Clickhouse REST API"},
            {"key": "Apache_Ofbiz_Identify", "value": "37. 发现 Apache Ofbiz"},
            {"key": "Apache_Apereo_CAS_Identify", "value": "38. 发现 Apache Apereo Cas"},
            {"key": "Any800_Identify", "value": "39. 发现 Any800全渠道智能客服云平台"},
            {"key": "Adminer_PHP_Identify", "value": "40. 发现 Adminer.php"}
        ]

        return utils.return_msg(200, "poc配置列表", data)


@ns.route('/get_weak_password')
class PortScanTypeTask(ARLResource):
    @auth
    def get(self):
        """
        获取弱口令爆破配置列表-字典
        """
        data = [
            {"key": "TomcatBrute", "value": "1. Tomcat 弱口令"},
            {"key": "Shiro_GCM_Brute", "value": "2. Shiro GCM 弱密钥"},
            {"key": "Shiro_CBC_Brute", "value": "3. Shiro CBC 弱密钥"},
            {"key": "SSHBrute", "value": "4. SSH 弱口令"},
            {"key": "SQLServerBrute", "value": "5. SQLServer 弱口令"},
            {"key": "SMTPBrute", "value": "6. SMTP 弱口令"},
            {"key": "RedisBrute", "value": "7. Redis 弱口令"},
            {"key": "RDPBrute", "value": "8. RDP 弱口令"},
            {"key": "PostgreSQLBrute", "value": "9. PostgreSQL 弱口令"},
            {"key": "POP3Brute", "value": "10. POP3 弱口令"},
            {"key": "OpenfireBrute", "value": "11. Openfire 弱口令"},
            {"key": "NexusBrute", "value": "12. Nexus Repository 弱口令"},
            {"key": "NacosBrute", "value": "13. Nacos 弱口令"},
            {"key": "MysqlBrute", "value": "14. MySQL 弱口令"},
            {"key": "MongoDBBrute", "value": "15. MongoDB 弱口令"},
            {"key": "JenkinsBrute", "value": "16. Jenkins 弱口令"},
            {"key": "IMAPBrute", "value": "17. IMAP 弱口令"},
            {"key": "HarborBrute", "value": "18. Harbor 弱口令"},
            {"key": "GrafanaBrute", "value": "19. Grafana 弱口令"},
            {"key": "GitlabBrute", "value": "20. Gitlab 弱口令"},
            {"key": "FTPBrute", "value": "21. FTP 弱口令"},
            {"key": "ExchangeBrute", "value": "22. Exchange 邮件服务器弱口令"},
            {"key": "CobaltStrikeBrute", "value": "23. CobaltStrike 弱口令"},
            {"key": "ClickhouseBrute", "value": "24. Clickhouse 弱口令"},
            {"key": "AlibabaDruidBrute", "value": "25. Alibaba Druid 弱口令"},
            {"key": "ActiveMQBrute", "value": "26. ActiveMQ 弱口令"},
            {"key": "APISIXBrute", "value": "27. APISIX 弱口令"}
        ]

        return utils.return_msg(200, "弱口令爆破配置列表", data)


@ns.route('/')
class ARLPolicy(ARLResource):
    parser = get_arl_parser(base_search_fields, location='args')

    @auth
    @ns.expect(parser)
    def get(self):
        """
        策略信息查询
        """
        args = self.parser.parse_args()
        data = self.build_data(args=args, collection='policy')

        return data


'''域名相关配置选项'''
domain_config_fields = ns.model('domainConfig', {
    "domain_brute": fields.Boolean(description="域名爆破", default=True),
    "domain_brute_type": fields.String(description="域名爆破类型(big)", example="big"),
    "alt_dns": fields.Boolean(description="DNS字典智能生成", default=True),
    "arl_search": fields.Boolean(description="ARL 历史查询", default=True),
    "dns_query_plugin": fields.Boolean(description="域名插件查询", default=False)
})

'''IP 相关配置选项'''
ip_config_fields = ns.model('ipConfig', {
    "port_scan": fields.Boolean(description="端口扫描", default=True),
    "port_scan_type": fields.String(description="端口扫描类型(test|top100|top1000|all|custom)", example="test"),
    "service_detection": fields.Boolean(description="服务识别", default=False),
    "os_detection": fields.Boolean(description="操作系统识别", default=False),
    "ssl_cert": fields.Boolean(description="SSL 证书获取", default=False),
    "skip_scan_cdn_ip": fields.Boolean(description="跳过 CDN IP扫描", default=True),  # 这个参数强制生效
    "port_custom": fields.String(description="自定义扫描端口", default="80,443"),  # 仅端口扫描类型为 custom 时生效
    "host_timeout_type": fields.String(description="主机超时时间类别（default|custom）", default="default"),
    "host_timeout": fields.Integer(description="主机超时时间(s)", default=900),
    "port_parallelism": fields.Integer(description="探测报文并行度", default=32),
    "port_min_rate": fields.Integer(description="最少发包速率", default=60)
})

'''站点相关配置选项'''
site_config_fields = ns.model('siteConfig', {
    "site_identify": fields.Boolean(description="站点识别", default=False),
    "site_capture": fields.Boolean(description="站点截图", default=False),
    "search_engines": fields.Boolean(description="搜索引擎调用", default=False),
    "site_spider": fields.Boolean(description="站点爬虫", default=False),
    "nuclei_scan": fields.Boolean(description="nuclei 扫描", default=False),
})

'''资产组关联配置'''
scope_config_fields = ns.model('scopeConfig', {
    "scope_id": fields.String(description="资产分组 ID", default=""),
})

add_policy_fields = ns.model('addPolicy', {
    "name": fields.String(required=True, description="策略名称"),
    "desc": fields.String(description="策略描述信息"),
    "policy": fields.Nested(ns.model("policy", {
        "domain_config": fields.Nested(domain_config_fields),
        "ip_config": fields.Nested(ip_config_fields),
        "site_config": fields.Nested(site_config_fields),
        "file_leak": fields.Boolean(description="文件泄漏", default=False),
        "npoc_service_detection": fields.Boolean(description="服务识别（纯python实现）", default=False),
        "poc_config": fields.List(fields.Nested(ns.model('pocConfig', {
            "plugin_name": fields.String(description="poc 插件名称ID", default=False),
            "enable": fields.Boolean(description="是否启用", default=True)
        }))),
        "brute_config": fields.List(fields.Nested(ns.model('bruteConfig', {
            "plugin_name": fields.String(description="poc 插件名称ID", default=False),
            "enable": fields.Boolean(description="是否启用", default=True)
        }))),
        "scope_config": fields.Nested(scope_config_fields)
    }, required=True)
                            )
})


@ns.route('/add/')
class AddARLPolicy(ARLResource):

    @auth
    @ns.expect(add_policy_fields)
    def post(self):
        """
        策略添加
        """
        args = self.parse_args(add_policy_fields)
        name = args.pop("name")
        policy = args.pop("policy", {})
        if policy is None:
            return utils.build_ret("Missing policy parameter", {})

        domain_config = policy.pop("domain_config", {})
        domain_config = self._update_arg(domain_config, domain_config_fields)
        ip_config = policy.pop("ip_config", {})
        port_scan_type = ip_config.get("port_scan_type", "test")
        if port_scan_type == "custom":
            port_custom = ip_config.get("port_custom", "80,443")
            port_list = utils.arl.build_port_custom(port_custom)
            if isinstance(port_list, str):
                return utils.build_ret(ErrorMsg.PortCustomInvalid, {"port_custom": port_list})

            ip_config["port_custom"] = ",".join(port_list)

        ip_config = self._update_arg(ip_config, ip_config_fields)

        site_config = policy.pop("site_config", {})
        site_config = self._update_arg(site_config, site_config_fields)

        poc_config = policy.pop("poc_config", [])
        if poc_config is None:
            poc_config = []

        poc_config = _update_plugin_config(poc_config)
        if isinstance(poc_config, str):
            return utils.build_ret(poc_config, {})

        brute_config = policy.pop("brute_config", [])
        if brute_config is None:
            brute_config = []
        brute_config = _update_plugin_config(brute_config)
        if isinstance(brute_config, str):
            return utils.build_ret(brute_config, {})

        file_leak = fields.boolean(policy.pop("file_leak", False))
        npoc_service_detection = fields.boolean(policy.pop("npoc_service_detection", False))
        desc = args.pop("desc", "")

        # 只要获得关联资产组的配置
        scope_config = policy.pop("scope_config", {})
        scope_config = self._update_arg(scope_config, scope_config_fields)

        item = {
            "name": name,
            "policy": {
                "domain_config": domain_config,
                "ip_config": ip_config,
                "site_config": site_config,
                "poc_config": poc_config,
                "brute_config": brute_config,
                "file_leak": file_leak,
                "npoc_service_detection": npoc_service_detection,
                "scope_config": scope_config
            },
            "desc": desc,
            "update_date": utils.curr_date()
        }
        utils.conn_db("policy").insert_one(item)

        return utils.build_ret(ErrorMsg.Success, {"policy_id": str(item["_id"])})

    def _update_arg(self, arg_dict, default_module):
        default_dict = get_dict_default_from_module(default_module)
        if arg_dict is None:
            return default_dict

        default_dict.update(arg_dict)

        for x in default_dict:
            if x not in default_module:
                continue

            default_dict[x] = default_module[x].format(default_dict[x])

        return default_dict


def plugin_name_in_arl(name):
    query = {
        "plugin_name": name
    }
    item = utils.conn_db('poc').find_one(query)
    return item


def get_dict_default_from_module(module):
    ret = {}
    for x in module:
        v = module[x]
        ret[x] = None
        if v.default is not None:
            ret[x] = v.default

        if v.example is not None:
            ret[x] = v.example

    return ret


delete_policy_fields = ns.model('DeletePolicy', {
    'policy_id': fields.List(fields.String(required=True, description="策略ID", example="603c65316591e73dd717d176"))
})


@ns.route('/delete/')
class DeletePolicy(ARLResource):
    @auth
    @ns.expect(delete_policy_fields)
    def post(self):
        """
        策略删除
        """
        args = self.parse_args(delete_policy_fields)
        policy_id_list = args.pop('policy_id')
        for policy_id in policy_id_list:
            if not policy_id:
                continue
            utils.conn_db('policy').delete_one({'_id': ObjectId(policy_id)})

        """这里直接返回成功了"""
        return utils.build_ret(ErrorMsg.Success, {})


edit_policy_fields = ns.model('editPolicy', {
    'policy_id': fields.String(required=True, description="策略ID", example="603c65316591e73dd717d176"),
    'policy_data': fields.Nested(ns.model("policyData", {}))
})


@ns.route('/edit/')
class EditPolicy(ARLResource):
    @auth
    @ns.expect(edit_policy_fields)
    def post(self):
        """
        策略编辑
        """
        args = self.parse_args(edit_policy_fields)
        policy_id = args.pop('policy_id')
        policy_data = args.pop('policy_data', {})
        query = {'_id': ObjectId(policy_id)}
        item = utils.conn_db('policy').find_one(query)

        if not item:
            return utils.build_ret(ErrorMsg.PolicyIDNotFound, {})

        if not policy_data:
            return utils.build_ret(ErrorMsg.PolicyDataIsEmpty, {})
        item = change_dict(item, policy_data)

        poc_config = item["policy"].pop("poc_config", [])
        poc_config = _update_plugin_config(poc_config)
        if isinstance(poc_config, str):
            return utils.build_ret(poc_config, {})
        item["policy"]["poc_config"] = poc_config

        brute_config = item["policy"].pop("brute_config", [])
        brute_config = _update_plugin_config(brute_config)
        if isinstance(brute_config, str):
            return utils.build_ret(brute_config, {})
        item["policy"]["brute_config"] = brute_config

        item["update_date"] = utils.curr_date()
        utils.conn_db('policy').find_one_and_replace(query, item)
        item.pop('_id')

        return utils.build_ret(ErrorMsg.Success, {"data": item})


def _update_plugin_config(config):
    plugin_name_set = set()
    ret = []
    for item in config:
        plugin_name = str(item.get("plugin_name", ""))
        enable = item.get("enable", False)
        if plugin_name is None or enable is None:
            continue
        if plugin_name in plugin_name_set:
            continue

        plugin_info = plugin_name_in_arl(plugin_name)
        if not plugin_info:
            return "没有找到 {} 插件".format(plugin_name)

        config_item = {
            "plugin_name": plugin_name,
            "vul_name": plugin_info["vul_name"],
            "enable": bool(enable)
        }
        plugin_name_set.add(plugin_name)
        ret.append(config_item)

    return ret


def change_dict(old_data, new_data):
    if not isinstance(new_data, dict):
        return

    for key in old_data:
        if key in ["_id", "update_date"]:
            continue

        next_old_data = old_data[key]
        next_new_data = new_data.get(key)
        if next_new_data is None:
            continue

        next_new_data_type = type(next_new_data)
        next_old_data_type = type(next_old_data)

        if isinstance(next_old_data, dict):
            change_dict(next_old_data, next_new_data)

        elif isinstance(next_old_data, list) and isinstance(next_new_data, list):
            old_data[key] = next_new_data

        elif next_new_data_type == next_old_data_type:
            old_data[key] = next_new_data

    return old_data  # 返回data
