from __future__ import absolute_import, division, print_function

__metaclass__ = type


class SVIArgs(object):
    """The arg spec for the sonic_interfaces module
    """

    def __init__(self, **kwargs):
        pass

    argument_spec = {
        "config": {
            "elements": "dict",
            "options": {
                "ip_address": {"type": "str"},  # 10.4.4.4/24
                "vlan_id": {"type": "str", "required": True}
                # "vlan_range": {"type": "int", "required": True}
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
        "commands": {"elements": "str", "type": "list"},
        "diff": {"elements": "str", "type": "list"}
    }
