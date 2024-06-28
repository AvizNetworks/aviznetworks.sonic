from __future__ import absolute_import, division, print_function

__metaclass__ = type


class SAGArgs(object):  # Static anycast gateway
    """The arg spec for the sonic_sag module

    """

    def __init__(self, **kwargs):
        pass

    argument_spec = {
        "config": {
            "options": {
                "mac_address": {"type": "str", "default": ""},
                "enable_ipv4": {"type": "bool", "default": None},
                "enable_ipv6": {"type": "bool", "default": None},
            },
            "type": "dict"
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
