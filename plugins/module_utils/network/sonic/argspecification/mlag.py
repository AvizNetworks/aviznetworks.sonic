from __future__ import absolute_import, division, print_function

__metaclass__ = type


class MlagArgs(object):
    """The arg spec for the sonic_interfaces module
    """

    def __init__(self, **kwargs):
        pass

    argument_spec = {
        "config": {
            "elements": "dict",
            "options": {
                "domain_id": {"type": "str", "required": True},
                "peer_address": {"type": "str", "default": ""},  # 10.4.5.2
                "src_address": {"type": "str", "default": ""},  # 10.4.5.2
                "peer_link": {"type": "str", "default": ""},  # portchannel200 / pch100 / 300 / Ethernet200
                "member_portchannels": {"type": "list", "default": []},  # portchannel200 / pch100 / 300
                "local_interface": {"type": "str", "default": ""}
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
