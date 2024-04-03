"""
The arg spec for the sonic_bgp_neighbors module
"""

from __future__ import absolute_import, division, print_function
__metaclass__ = type


class BGPAddressFamilyArgs(object):
    def __init__(self, **kwargs):
        pass

    argument_spec = {
        "config": {
            "options": {
                "bgp_asn": {"required": True, "type": "str"},
                "address_family": {
                    "options": {
                        "ipv4": {
                            "elements": "dict",
                            "options": {
                                "neighbor_ip": {"required": True, "type": "list"},
                                "allowas_in": {"type": "int", "default": None},
                                "activate": {"type": "bool", "default": None},
                                "network" : {"type": "list", "default": None},
                                "redistribute": {"type": "list", "default": None},
                                "route_reflector_client": {"type": "bool", "default": None},
                                "next_hop_self": {"type": "bool", "default": None},
                            },
                            "type": "list"
                        },
                        "ipv6": {
                            "elements": "dict",
                            "options": {
                                "neighbor_ip": {"required": True,"type": "str"},
                                "allowas_in": {"type": "int", "default": None},
                                "activate": {"type": "bool", "default": None},
                            },
                            "type": "list"
                        },
                    },
                    "type": "dict"
                },
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


  