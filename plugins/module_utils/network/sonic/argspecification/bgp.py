"""
The arg spec for the sonic_bgp_neighbors module
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class BGPArgs(object):
    def __init__(self, **kwargs):
        pass

    argument_spec = {
        "config": {
            "options": {
                "bgp_asn": {"required": True, "type": "str"},
                "bgp": {
                    "elements": "dict",
                    "options": {
                        "router_id": {"type": "str"},
                        "bestpath": {"type": "bool", "default": None},
                        "ebgp_requires_policy": {"type": "bool", "default": False},
                        "restart_time": {"type": "int", "default": None},
                        "stalepath_time": {"type": "int", "default": None},
                    },
                    "type": "list"
                }
            },
            "type": "dict"
        },
        "state": {
            "choices": ["merged", "deleted"],
            "default": "merged"
        },
        "wait_for": {"elements": "str", "type": "list"},
        "match": {"default": "all", "choices": ["all", "any"]},
        "retries": {"default": 10, "type": "int"},
        "interval": {"default": 3, "type": "int"},
        "commands": {"elements": "str", "type": "list"}
    }
