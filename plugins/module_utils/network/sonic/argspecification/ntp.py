from __future__ import absolute_import, division, print_function

__metaclass__ = type


class NTPArgs(object):
    """The arg spec for the sonic_interfaces module
    """

    def __init__(self, **kwargs):
        pass

    argument_spec = {
        "config": {
            "options": {
                "ipv4": {"type": "str", "default": ""},
                "ipv6": {"type": "str", "default": ""},
                "timezone": {"type": "str", "default": ""}
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
        "commands": {"elements": "str", "type": "list"},
        "diff": {"elements": "str", "type": "list"}

    }
