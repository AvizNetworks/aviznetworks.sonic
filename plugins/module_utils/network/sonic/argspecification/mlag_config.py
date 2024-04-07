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
                "domain_id": {"type": "str", "required": False},
                "peer_address": {"type": "str",  "required": False},
                "peer_link": {"type": "str", "required": False},
                "src_address": {"type": "str", "required": False},
                "member_port_channel": {"type": "list", "required": False},
                "local_interface": {"type": "str", "required": False}
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
        "commands": {"elements": "str" , "type": "list"},
        "diff": {"elements": "str" , "type": "list"}

    }