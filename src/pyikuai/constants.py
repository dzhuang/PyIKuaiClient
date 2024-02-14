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
    sysstat = "sysstat"
    macgroup = "macgroup"
    acl_l7 = "acl_l7"
    domain_blacklist = "domain_blacklist"
    monitor_lanip = "monitor_lanip"
    monitor_lanipv6 = "monitor_lanipv6"


class rp_order_param:  # noqa
    asc = "asc"
    desc = "desc"


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
