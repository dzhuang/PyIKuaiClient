# PyIKuaiClient

A Python client for interacting with IKuai routers.

## How to install

```bash
pip install pyikuai
```

## Usage

```python
from pyikuai import IKuaiClient

ikuai_client = IKuaiClient(
    url="http://192.168.1.1",
    username="your/ikuai/username",
    password="your/ikuai/password"
)

```

## Implemented functionality

### mac_group

```python

>>> ikuai_client.list_mac_groups()  # get the mac_groups configured
{'total': 2,
 'data': [{'id': 1,
   'comment': '',
   'group_name': 'IPAD',
   'addr_pool': '34:b8:ec:42:91:2d'},
  {'id': 2,
   'comment': 'foo,%20bar',
   'group_name': 'test',
   'addr_pool': '43:a9:fc:43:97:3d,43:a9:fc:43:97:3f'}]}
>>> ikuai_client.del_mac_group(group_id=3)  # delete mac_group with id 3
{'Result': 30000, 'ErrMsg': 'Success'}  # succeed even that id does not exists.
>>> ikuai_client.add_mac_group(
    group_name="test2",
    addr_pools=['43:a9:fc:43:97:3d', '43:a9:fc:43:97:3f'],
    comments=["foo2", "bar2"])

{'Result': 30000, 'ErrMsg': 'Success', 'RowId': 3}
>>> ikuai_client.edit_mac_group(  # update mac_group id 3 with new comments
    group_id=3,
    group_name="test2", 
    addr_pools=['43:a9:fc:43:97:3d', '43:a9:fc:43:97:3f'],
    comments=["foo3", "bar3"])

{'Result': 30000, 'ErrMsg': 'Success'}
```

### acl_l7

The functionality related to behavioral control of devices connected, via protocol. 
The implemented methods include
`add_acl_l7`, `list_acl_l7`, `edit_acl_l7`, `del_acl_l7`, `disable_acl_l7`, `enable_acl_l7`.


### domain_blacklist

The functionality related to behavioral control of devices connected, via domain blacklist.
The implemented methods include
`add_domain_blacklist`, `list_domain_blacklist`, `edit_domain_blacklist`, `del_domain_blacklist`,
`disable_domain_blacklist`, `enable_domain_blacklist`


### sysstat

Get the system statistics. 

```python
>>> ikuai_client.get_sysstat()
{'verinfo': {'modelname': '',
  'verstring': '3.7.10 x32 Build202401231339',
  'version': '3.7.10',
  'build_date': 202401231339,
  'arch': 'x86',
  'sysbit': 'x32',
  'verflags': '',
  'is_enterprise': 0,
  'support_i18n': 0,
  'support_dingtalk': 1,
  'support_lcd': 0,
  'bootguide': 'hd'},
 'cpu': ['0.00%', '0.00%'],
 'memory': {'total': 886264,
  'available': 618720,
  'free': 538644,
  'cached': 45460,
  'buffers': 69132,
  'used': '30%'},
 'stream': {'connect_num': 52,
  'upload': 821,
  'download': 432,
  'total_up': 671137724,
  'total_down': 4459837833},
 'cputemp': []}
>>> ikuai_client.get_sysstat(["verinfo"])
{'verinfo': {'modelname': '',
  'verstring': '3.7.10 x32 Build202401231339',
  'version': '3.7.10',
  'build_date': 202401231339,
  'arch': 'x86',
  'sysbit': 'x32',
  'verflags': '',
  'is_enterprise': 0,
  'support_i18n': 0,
  'support_dingtalk': 1,
  'support_lcd': 0,
  'bootguide': 'hd'}}
```

### monitor_lanip & monitor_lanipv6

Get the monitor list of lanip (v4) or lanipv6. For v4, use ``ikuai_client.list_monitor_lanip()``. For v6, use ``ikuai_client.list_monitor_lanip(ip_type='v6')`` .


### acl_mac

The access control of device via mac address. The implemented methods include: `add_acl_mac`, `list_acl_mac`, `edit_acl_mac`, `del_acl_mac`, `enable_acl_mac`, `disable_acl_mac`.

### mac_comment

The management of alias of devices, mapping mac addresses. The implemented methods include: `add_mac_comment`, `list_mac_comment`, `edit_mac_comment`, `del_mac_comment`.

### mac_qos

The interface for limiting download/upload speed of devices, mapping mac addresses. The implemented methods include: `add_mac_qos`, `list_mac_qos`, `edit_mac_qos`, `del_mac_qos`, `enable_mac_qos`, `disable_mac_qos`.
