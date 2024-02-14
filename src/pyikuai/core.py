import base64
import hashlib
import json
from datetime import datetime
from urllib.parse import quote, urljoin

import requests

from .constants import (JSON_RESPONSE_DATA, JSON_RESPONSE_ERRMSG,
                        JSON_RESPONSE_ERRMSG_SUCCESS, JSON_RESPONSE_RESULT,
                        acl_l7_param, acl_l7_param_action,
                        domain_blacklist_param, json_result_code,
                        mac_group_param, rp_action, rp_func_name, rp_key,
                        rp_order_param)
from .exceptions import (AuthenticationError, RequestError, RouterAPIError,
                         ValidationError)


class QueryRPParam:
    def __init__(
            self, param_type: list | None = None,
            limit=None, order_by=None, order_param=None):
        """
        :param param_type: list
        :param limit: list of int
        :param order_by: string
        :param order_param: string
        """

        if param_type is not None:
            assert isinstance(param_type, list), "param_type must be a list"
        self.param_type = param_type or ["total", "data"]

        if limit is not None:
            assert isinstance(limit, list), "limit must be a list"
            assert len(limit) == 2,  (
                "limit must be a list with 2 elements which denote "
                "start number and end number")
        self.limit = limit or [0, 100]

        if order_by:
            assert isinstance(order_by, str), (
                "order_by must be a string which denote the field to be sorted")
        self.order_by = order_by or ""

        if order_param:
            assert isinstance(order_param, str), (
                "order_param must be a string which denote how the field "
                "will be sorted")
            assert order_param in [rp_order_param.asc, rp_order_param.desc]
        self.order_param = order_param or ""

    def as_dict(self):
        return {
            "TYPE": ",".join(self.param_type),
            "limit": ",".join(map(str, self.limit)),
            "ORDER_BY": self.order_by,
            "ORDER": self.order_param
        }


class IKuaiClient:  # noqa
    def __init__(self, url, username, password):
        self._username = username
        self._passwd = password
        self.base_url = url.strip().rstrip("/")
        self._session = None

    @property
    def session(self):
        if self._session is None:
            self._session = requests.session()
            self.authenticate()

        return self._session

    def authenticate(self):
        passwd = hashlib.md5(self._passwd.encode()).hexdigest()
        pass_encoded = base64.b64encode(f'salt_11{passwd}'.encode()).decode()
        login_info = {
            'passwd': passwd,
            'pass': pass_encoded,
            'remember_password': "",
            'username': self._username
        }
        self._session = requests.session()

        response = (
            self._session.post(f'{self.base_url}/Action/login', json=login_info))
        if response.status_code != 200:
            self._session = None
            raise AuthenticationError(
                f"Failed to authenticate with status code {response.status_code}")

        content = response.json()
        if content[JSON_RESPONSE_RESULT] != json_result_code.code_10000:
            self._session = None
            raise AuthenticationError(
                "Failed to authenticate with result code "
                f"{content[JSON_RESPONSE_RESULT]}: {content[JSON_RESPONSE_ERRMSG]}."
            )

    def get_protocols_json(self):
        response = self.session.get(
            urljoin(self.base_url, "json/protocols_cn.json"), headers={
                "Content-Type": 'application/json'
            })
        if response.status_code == 200:
            return response.json()
        raise RequestError(
            f"Request failed with response status code: {response.status_code}")

    def exec(self, func_name, action, param, ensure_success=True):
        payload = {
            rp_key.func_name: func_name,
            rp_key.action: action,
            rp_key.param: param
        }
        response = self.session.post(
            urljoin(self.base_url, "/Action/call"), json=payload, headers={
                "Content-Type": 'application/json'
            })
        if response.status_code == 200:
            try:
                content = response.json()
                if not ensure_success:
                    return content

                if content[JSON_RESPONSE_ERRMSG] == JSON_RESPONSE_ERRMSG_SUCCESS:
                    return content
                else:
                    if content[JSON_RESPONSE_ERRMSG] == "no login authentication":
                        self._session = None
                        return self.exec(func_name, action, param, ensure_success)
                    raise RouterAPIError(
                        f"API result error: '{content[JSON_RESPONSE_ERRMSG]}': "
                        f"{repr(content)}"
                    )
            except json.JSONDecodeError:
                # the response is not a valid json
                if 'sending to kernel ...' in response.content.decode():
                    return json.loads(
                        response.content.decode().replace(
                            "sending to kernel ...", "").replace("\n", ""))

                raise RequestError(
                    f"Error parsing response: {response.content.decode()}")

        raise RequestError(
            f"Request failed with response status code: {response.status_code}")

    @staticmethod
    def validate_time_range(time_range_str):
        # 分割字符串以检查两个时间
        parts = time_range_str.split("-")
        if len(parts) != 2:
            raise ValidationError(
                "time format error: it must be of format 'HH:MM-HH:MM'")

        # 验证时间格式
        time_format = "%H:%M"
        start_time_str, end_time_str = parts
        try:
            # 尝试将字符串转换为时间对象以验证格式和范围
            start_time = datetime.strptime(start_time_str, time_format)  # noqa
            end_time = datetime.strptime(end_time_str, time_format)  # noqa
        except Exception as e:
            # 如果转换失败，说明时间格式不正确
            raise ValidationError(f"time format error: {type(e).__name__}: {str(e)}")

        # 可选: 检查开始时间是否早于或等于结束时间
        # if start_time > end_time:
        #     return False
        return

    # {{{ mac group CRUD

    def add_mac_group(self, group_name, addr_pools, comments=None):
        comments = comments or []
        return self.exec(
            func_name=rp_func_name.macgroup,
            action=rp_action.add,
            param={
                mac_group_param.newRow: True,
                mac_group_param.group_name: group_name,
                mac_group_param.addr_pool: ",".join(addr_pools),
                mac_group_param.comment: (f",{quote(' ')}".join(comments))
            }
        )

    def get_mac_groups(self, **query_kwargs):
        result = self.exec(
            func_name=rp_func_name.macgroup,
            action=rp_action.show,
            param=QueryRPParam(**query_kwargs).as_dict()
        )
        return result[JSON_RESPONSE_DATA]

    def edit_mac_group(self, group_id, group_name, addr_pools, comments=None):
        comments = comments or []
        return self.exec(
            func_name=rp_func_name.macgroup,
            action=rp_action.edit,
            param={
                mac_group_param.id: group_id,
                mac_group_param.group_name: group_name,
                mac_group_param.addr_pool: ",".join(addr_pools),
                mac_group_param.comment: (f",{quote(' ')}".join(comments))
            }
        )

    def del_mac_group(self, group_id):
        return self.exec(
            func_name=rp_func_name.macgroup,
            action=rp_action.delete,
            param={
                mac_group_param.id: group_id,
            }
        )

    # }}}

    # {{{ acl_l7 CRUD
    # 行为管控 之 应用协议控制

    def _get_acl_l7_param(
            self, comment, src_addrs: list, action,
            dst_addrs: list | None = None,
            prio=32, app_protos=None, enabled=True, time="00:00-23:59",
            week="1234567"):

        self.validate_time_range(time)

        app_protos = app_protos or []
        enabled = "yes" if enabled else "no"
        comment = comment.replace(" ", quote(" "))
        assert action in [acl_l7_param_action.accept, acl_l7_param_action.drop]

        dst_addrs = dst_addrs or []
        dst_addr = ",".join(dst_addrs)

        src_addr = ",".join(src_addrs)

        param = {
            acl_l7_param.action: action,
            acl_l7_param.app_proto: ",".join(app_protos),
            acl_l7_param.comment: comment,
            acl_l7_param.dst_addr: dst_addr or "",
            acl_l7_param.enabled: enabled,
            acl_l7_param.prio: prio,
            acl_l7_param.src_addr: src_addr,
            acl_l7_param.time: time,
            acl_l7_param.week: week
        }
        return param

    def add_acl_l7(self, comment, src_addrs, action, dst_addrs=None,
                   prio=32, app_protos=None, enabled=True, time="00:00-23:59",
                   week="1234567"):

        param = self._get_acl_l7_param(
            comment, src_addrs, action, dst_addrs, prio,
            app_protos, enabled, time, week)

        return self.exec(
            func_name=rp_func_name.acl_l7,
            action=rp_action.add,
            param=param
        )

    def get_acl_l7(self, **query_kwargs):
        result = self.exec(
            func_name=rp_func_name.acl_l7,
            action=rp_action.show,
            param=QueryRPParam(**query_kwargs).as_dict()
        )
        return result[JSON_RESPONSE_DATA]

    def edit_acl_l7(self, acl_l7_id, comment, src_addrs, action, dst_addrs=None,
                    prio=32, app_protos=None, enabled=True, time="00:00-23:59",
                    week="1234567"):
        param = self._get_acl_l7_param(
            comment, src_addrs, action, dst_addrs, prio,
            app_protos, enabled, time, week)

        param[acl_l7_param.id] = acl_l7_id

        return self.exec(
            func_name=rp_func_name.acl_l7,
            action=rp_action.edit,
            param=param
        )

    def del_acl_l7(self, acl_l7_id):
        return self.exec(
            func_name=rp_func_name.acl_l7,
            action=rp_action.delete,
            param={
                acl_l7_param.id: acl_l7_id,
            }
        )

    def disable_acl_l7(self, acl_l7_id):
        return self.exec(
            func_name=rp_func_name.acl_l7,
            action=rp_action.down,
            param={
                acl_l7_param.id: acl_l7_id,
            }
        )

    def enable_acl_l7(self, acl_l7_id):
        return self.exec(
            func_name=rp_func_name.acl_l7,
            action=rp_action.up,
            param={
                acl_l7_param.id: acl_l7_id,
            }
        )

    # }}}

    # {{{ domain_blacklist CRUD
    # 行为管控 之 禁止娱乐网站

    def _get_domain_blacklist_param(
            self, enabled=True,
            ipaddrs: list | None = None,
            domain_groups=None, time="00:00-23:59",
            comment=None,
            weekdays="1234567"):

        self.validate_time_range(time)

        domain_groups = domain_groups or []
        enabled = "yes" if enabled else "no"
        comment = comment or []
        comment = comment.replace(" ", quote(" "))

        ipaddrs = ipaddrs or []
        ipaddr = ",".join(ipaddrs)

        param = {
            domain_blacklist_param.comment: comment,
            domain_blacklist_param.domain_group: ",".join(domain_groups),
            domain_blacklist_param.enabled: enabled,
            domain_blacklist_param.ipaddr: ipaddr,
            domain_blacklist_param.time: time,
            domain_blacklist_param.weekdays: weekdays
        }
        return param

    def get_domain_blacklist(self, **query_kwargs):
        result = self.exec(
            func_name=rp_func_name.domain_blacklist,
            action=rp_action.show,
            param=QueryRPParam(**query_kwargs).as_dict()
        )
        return result[JSON_RESPONSE_DATA]

    def add_domain_blacklist(
            self, enabled=True,
            ipaddrs: list | None = None,
            domain_groups=None, time="00:00-23:59",
            comment=None,
            weekdays="1234567"):

        param = self._get_domain_blacklist_param(
            enabled=enabled,
            ipaddrs=ipaddrs,
            domain_groups=domain_groups,
            time=time,
            comment=comment,
            weekdays=weekdays)

        return self.exec(
            func_name=rp_func_name.domain_blacklist,
            action=rp_action.add,
            param=param
        )

    def edit_domain_blacklist(
            self, domain_blacklist_id, enabled=True,
            ipaddrs: list | None = None,
            domain_groups=None, time="00:00-23:59",
            comment=None,
            weekdays="1234567"):

        param = self._get_domain_blacklist_param(
            enabled=enabled,
            ipaddrs=ipaddrs,
            domain_groups=domain_groups,
            time=time,
            comment=comment,
            weekdays=weekdays)

        param[domain_blacklist_param.id] = domain_blacklist_id

        return self.exec(
            func_name=rp_func_name.domain_blacklist,
            action=rp_action.edit,
            param=param
        )

    def del_domain_blacklist(self, domain_blacklist_id):
        return self.exec(
            func_name=rp_func_name.domain_blacklist,
            action=rp_action.delete,
            param={
                domain_blacklist_param.id: domain_blacklist_id,
            }
        )

    def disable_domain_blacklist(self, domain_blacklist_id):
        return self.exec(
            func_name=rp_func_name.domain_blacklist,
            action=rp_action.down,
            param={
                domain_blacklist_param.id: domain_blacklist_id,
            }
        )

    def enable_domain_blacklist(self, domain_blacklist_id):
        return self.exec(
            func_name=rp_func_name.domain_blacklist,
            action=rp_action.up,
            param={
                domain_blacklist_param.id: domain_blacklist_id,
            }
        )

    # }}}

    def get_sysstat(self, param_types=None):
        param_types = param_types or "verinfo,cpu,memory,stream,cputemp".split(",")
        result = self.exec(
            func_name=rp_func_name.sysstat,
            action=rp_action.show,
            param={"TYPE": ",".join(param_types)}
        )
        return result[JSON_RESPONSE_DATA]

    def get_monitor_lanip(self, ip_type="v4", **query_kwargs):
        assert ip_type in ["v4", "v6"], "ip_type must be 'v4' or 'v6'"

        result = self.exec(
            func_name=(rp_func_name.monitor_lanip if ip_type == "v4"
                       else rp_func_name.monitor_lanipv6),
            action=rp_action.show,
            param=QueryRPParam(**query_kwargs).as_dict()
        )
        return result[JSON_RESPONSE_DATA]
