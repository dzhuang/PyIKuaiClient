JSON_RESPONSE_RESULT = "Result"
JSON_RESPONSE_ERRMSG = "ErrMsg"
JSON_RESPONSE_ERRMSG_SUCCESS = "Success"
JSON_RESPONSE_DATA = "Data"


class json_result_code:  # noqa
    code_10001 = 10001
    code_10000 = 10000
    code_30000 = 30000


class rp_key:  # noqa
    action = "action"
    func_name = "func_name"
    param = "param"


class rp_action:  # noqa
    show = "show"
    add = "add"
    edit = "edit"
    delete = "del"
    up = "up"
    down = "down"


class rp_func_name:  # noqa
    macgroup = "macgroup"
    acl_l7 = "acl_l7"


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
        self.param_type = param_type or ["data", "total"]
        self.limit = limit or [0, 100]
        self.order_by = order_by or ""
        self.order_param = order_param or ""

    def as_dict(self):
        return {
            "TYPE": ",".join(self.param_type),
            "limit": ",".join(map(str, self.limit)),
            "ORDER_BY": self.order_by,
            "ORDER": self.order_param
        }


class mac_group_param:  # noqa
    id = "id"
    group_name = "group_name"
    addr_pool = "addr_pool"
    comment = "comment"
    newRow = "newRow"


class acl_l7_param:  # noqa
    action = "action"
    app_proto = "app_proto"
    comment = "comment"
    dst_addr = "dst_addr"
    enabled = "enabled"
    id = "id"
    prio = "prio"
    src_addr = "src_addr"
    time = "time"
    week = "week"


class acl_l7_param_action:  # noqa
    drop = "drop"
    accept = "accept"
