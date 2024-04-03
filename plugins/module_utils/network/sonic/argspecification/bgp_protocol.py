"""
The arg spec for the sonic_bgp_neighbors module
"""

from __future__ import absolute_import, division, print_function
__metaclass__ = type


class BGPProtocolArgs(object):
    def __init__(self, **kwargs):
        pass

    argument_spec = {
        "config": {
            "options": {
                "protocol_bgp_route_map_name": {"type": "str"},
                "permit_no": {"type": "int"},
                "src_ip": {"type": "str"},
            },
            "type": "list"
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


  