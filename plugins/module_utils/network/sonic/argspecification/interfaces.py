from __future__ import absolute_import, division, print_function

__metaclass__ = type


class InterfacesArgs(object):
    """The arg spec for the sonic_interfaces module
    """

    def __init__(self, **kwargs):
        pass

    argument_spec = {
        "config": {
            "elements": "dict",
            "options": {
                "description": {"type": "str", "default": None},
                "enable": {"type": "bool", "default": None},
                "mtu": {"type": "int", "default": None},
                "ip_address": {"type": "str"},  # 10.4.4.4/24
                "interfaces": {"type": "list", "required": True},
                "autoneg": {"type": "bool", "default": None},  # not supported in fmcli
                "speed": {"type": "str",
                          "choices": ["1G",
                                      "10G",
                                      "25G",
                                      "40G",
                                      "50G",
                                      "100G",
                                      "400G"]
                          },
                "advertised_speed": {"type": "list", "elements": "str"},
                "fec": {"type": "str",
                        "choices": ["rs",
                                    "fc",
                                    "none"]}
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
