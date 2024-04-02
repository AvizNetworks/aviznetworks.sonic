from __future__ import absolute_import, division, print_function

__metaclass__ = type


class PortchannelArgs(object):
    """The arg spec for the sonic_interfaces module
    """

    def __init__(self, **kwargs):
        pass

    argument_spec = {
        "config": {
            "elements": "dict",
            "options": {
                "pch_id": {"type": "str", "required": True},
                "interfaces": {"type": "list"},
                "description": {"type": "str"},
                "mtu": {"type": "str"},
                "ip_address": {"type": "str"},
                "speed": {"type": "str",
                          "choices": ["1G",
                                      "10G",
                                      "25G",
                                      "40G",
                                      "50G",
                                      "100G",
                                      "400G"]
                                      },
                "mode": {"type": "str",
                    "choices": ["active", "static"]
                },
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