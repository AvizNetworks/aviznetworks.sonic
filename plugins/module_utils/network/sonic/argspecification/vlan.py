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
                "vlan_id": {"type": "list", "required": True},
                "interface": {"type": "list", "default": None},
                "vlan_mode": {"type": "str", "default": None},
                "ipaddress": {"type": "str", "default": None},
                "enableswitchport": {"type": "bool", "default": True},
            },
            "type": "list"
        },
        "state": {
            "choices": ["merge", "replace", "override", "delete"],
            "default": "merge",
            "type": "str"
        },
        "wait_for": {"elements": "str" , "type": "list"},
        "match": {"default": "all", "choices":["all", "any"]},
        "retries": {"default": 10, "type": "int"},
        "interval": {"default": 1, "type": "int"},
        "commands": {"elements": "str" , "type": "list"}
    }