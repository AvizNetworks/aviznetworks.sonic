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
            "elements": "dict",
            "options": {
                "bgp_asn": {"required": True, "type": "str"},
                "address_family": {
                    "options": {
                        "ipv4": {
                            # "elements": "dict",
                            "options": {
                                "neighbor": {
                                    "options": {
                                        # "neighbor_address": {
                                        #     "options": {
                                        "ips": {"type": "list", "default": []},
                                        "activate": {"type": "bool", "default": None},
                                        "allowas_in": {"type": "int", "default": None},
                                        "filter_list": {
                                            "options": {
                                                "accesslistname": {"type": "str"},
                                                'choices': ['in', 'out'],
                                            },
                                            "type": "dict"
                                        },
                                        "route_map": {
                                            "options": {
                                                "route_map_name": {"type": "str"},
                                                'choices': ['in', 'out'],
                                            },
                                            "type": "dict"
                                        },
                                        "next_hop_self": {"type": "bool", "default": None},
                                        "route_reflector_client": {"type": "bool", "default": None},
                                        "send-community": {
                                            "options": {
                                                'choices': ['all', 'both', 'extended', 'large', 'standard'],
                                            },
                                            "type": "dict"
                                        },
                                    },
                                    "type": "dict"
                                    #     }, 
                                    # },
                                    # "type": "dict"
                                },
                                "network": {"type": "list", "default": None},
                                "redistribute": {"type": "list", "default": None},
                            },
                            "type": "dict"
                        }
                    },
                    "type": "dict"
                }
            },
            "type": "list"
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
