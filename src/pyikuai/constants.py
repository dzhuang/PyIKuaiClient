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
    domain_blacklist = "domain_blacklist"
    monitor_lanip = "monitor_lanip"


class rp_order_param:  # noqa
    asc = "asc"
    desc = "desc"


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


class mac_group_param:  # noqa
    id = "id"
    group_name = "group_name"
    addr_pool = "addr_pool"
    comment = "comment"
    newRow = "newRow"


class acl_l7_param:  # noqa
    id = "id"
    action = "action"
    app_proto = "app_proto"
    comment = "comment"
    dst_addr = "dst_addr"
    enabled = "enabled"
    prio = "prio"
    src_addr = "src_addr"
    time = "time"
    week = "week"


class acl_l7_param_action:  # noqa
    drop = "drop"
    accept = "accept"


class domain_blacklist_param:  # noqa
    id = "id"
    comment = "comment"
    domain_group = "domain_group"
    enabled = "enabled"
    ipaddr = "ipaddr"
    time = "time"
    weekdays = "weekdays"
