"""
The arg spec for the sonic_bgp_neighbors module
"""

from __future__ import absolute_import, division, print_function
__metaclass__ = type


class BGPNeighborsArgs(object):
    def __init__(self, **kwargs):
        pass

    argument_spec = {
        "config": {
            "options": {
                "bgp_asn": {"required": True, "type": "str"},
                "neighbor": {
                    "elements": "dict",
                    "options": {
                        "neighbor_ip": {"required": True, "type": "list"},
                        "remote_as": {"type": "str"},
                        "extended_nexthop": {"type": "bool", "default": None},
                        "peer_group_name": {"type": "str"},
                        "bfd": {"type": "str"},
                        "shoutdown": {"type": "bool", "default": None},
                        "timers": {
                            "options": {
                                "holdtime": {"type": "int"},
                                "keepalive": {"type": "int"}
                            },
                            "type": "dict"
                        },
                        "update_source": {
                            "options": {
                                "interface": {"type": "str"},
                                "portchannel": {"type": "str"}
                            },
                            "type": "dict"
                        }
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
        "wait_for": {"elements": "str" , "type": "list"},
        "match": {"default": "all", "choices":["all", "any"]},
        "retries": {"default": 10, "type": "int"},
        "interval": {"default": 3, "type": "int"},
        "commands": {"elements": "str" , "type": "list"}
    }


  