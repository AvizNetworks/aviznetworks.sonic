from __future__ import absolute_import, division, print_function

__metaclass__ = type


class EvpnMHArgs(object):
    """The arg spec for the sonic_interfaces module
    """

    def __init__(self, **kwargs):
        pass

    argument_spec = {
        "config": {
            "elements": "dict",
            "options": {
                "es_id": {"type": "str", "default": ""},  # Ethernet segment ID
                "es_sys_mac": {"type": "str", "default": ""},  # ES System MAC
                "uplink": {"type": "bool", "default": None},
                "interface": {"type": "str", "default": ""}  # pch10 / portchannel20 / Ethernet4
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
