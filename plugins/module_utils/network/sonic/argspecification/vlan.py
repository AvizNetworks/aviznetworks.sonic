from __future__ import absolute_import, division, print_function

__metaclass__ = type


class VlanArgs(object):
    """The arg spec for the sonic_interfaces module
    """

    def __init__(self, **kwargs):
        pass

    argument_spec = {
        "config": {
            "elements": "dict",
            "options": {
                "vlan_ids": {"type": "list"},
                "vlan_id": {"type": "str"},
                "name": {"type": "str"},
                # "description": {"type": "str", "default": ""},
                "vrf_name": {"type": "str", "default": ""},
                "interfaces": {"type": "list", "default": []},  # portchannel10 / Ethernet10
                "vlan_mode": {"type": "str", "default": ""},
                "pch_ids": {"type": "list", "default": []},
                "ip_address": {"type": "str"},  # 10.4.4.4/24
                "anycast_gateway": {"type": "str"}  # 10.4.4.4/24
            },
            "type": "list"
        },
        "state": {
            "choices": ["merge", "replace", "override", "delete"],
            "default": "merge",
            "type": "str"
        },
        "wait_for": {"elements": "str", "type": "list"},
        "match": {"default": "all", "choices": ["all", "any"]},
        "retries": {"default": 10, "type": "int"},
        "interval": {"default": 1, "type": "int"},
        "commands": {"elements": "str", "type": "list"}
    }
