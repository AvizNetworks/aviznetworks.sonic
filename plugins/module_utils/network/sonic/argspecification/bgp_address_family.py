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
                            "options": {
                                "neighbor": {
                                    "options": {
                                        "ips": {"type": "list", "default": []},
                                        "activate": {"type": "bool", "default": None},
                                        # Enable the Address Family for this Neighbor
                                        "allowas_in": {"type": "str", "default": ""},
                                        # Accept as-path with my AS present in it
                                        # "allowas_in": {
                                        #     "options": {
                                        #         "as_occurrence": {"type": "str",
                                        #         "choices": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "origin", "None"]},
                                        #     },"type": "dict"
                                        # }, # as_occurrence
                                        "filter_list": {
                                            "options": {
                                                "access_list_name": {"type": "str",
                                                                     "choices": ["in", "out"]},
                                            },
                                            "type": "dict"
                                        },
                                        "route_map": {
                                            "options": {
                                                "route_map_name": {"type": "str",
                                                                   "choices": ["in", "out"]},
                                            },
                                            "type": "dict"
                                        },
                                        "next_hop_self": {"type": "bool", "default": None},
                                        "route_reflector_client": {"type": "bool", "default": None},
                                        "send_community": {
                                            "type": "str",
                                            "choices": ["all", "both", "extended", "large", "standard"],
                                        },
                                    },
                                    "type": "dict"
                                },
                                "network": {"type": "list", "default": []},
                                "redistribute": {"type": "list", "default": []},
                                "max_path": {"type": "str", "default": ""},
                                "aggregate_address": {}  # [in progress]
                            },
                            "type": "dict"
                        },
                        "ipv6": {
                            "options": {
                                "neighbor": {
                                    "options": {
                                        "ips": {"type": "list", "default": []},
                                        "activate": {"type": "bool", "default": None},
                                        "allowas_in": {
                                            "options": {
                                                "as_occurrence": {"type": "str",
                                                                  "choices": ["1", "2", "3", "4", "5", "6", "7", "8",
                                                                              "9", "10", "origin",
                                                                              "None"]},
                                            },
                                            "type": "dict"
                                        },
                                        "filter_list": {
                                            "options": {
                                                "accesslistname": {"type": "str",
                                                                   "choices": ["in", "out"]},
                                            },
                                            "type": "dict"
                                        },
                                        "route_map": {
                                            "options": {
                                                "route_map_name": {"type": "str",
                                                                   "choices": ["in", "out"]},
                                            }
                                            # "type": "dict"
                                        },
                                        "next_hop_self": {"type": "bool", "default": None},
                                        "route_reflector_client": {"type": "bool", "default": None},
                                        "send_community": {
                                            "type": "str",
                                            "choices": ["all", "both", "extended", "large", "standard"]
                                        },
                                    },
                                    "type": "dict"
                                },
                                "network": {"type": "list", "default": []},
                                "redistribute": {"type": "list", "default": []},
                                "max_path": {"type": "str", "default": ""},
                                "aggregate_address": {}
                            },
                            "type": "dict"
                        },
                        "l2vpn": {
                            "options": {
                                "neighbor": {
                                    "options": {
                                        "ips": {"type": "list", "default": []},
                                        "activate": {"type": "bool", "default": None},
                                        "allowas_in": {
                                            "options": {
                                                "as_occurrence": {"type": "str",
                                                                  "choices": ["1", "2", "3", "4", "5", "6", "7", "8",
                                                                              "9", "10", "origin",
                                                                              "None"]}
                                            },
                                            "type": "dict"

                                        },

                                        "filter_list": {
                                            "options": {
                                                "accesslistname": {"type": "str",
                                                                   "choices": ["in", "out"]},
                                            },
                                            "type": "dict"
                                        },
                                        "route_map": {
                                            "options": {
                                                "route_map_name": {"type": "str"},
                                                "choices": ["in", "out"],
                                            },
                                            "type": "dict"
                                        },
                                        "next_hop_self": {"type": "bool", "default": None},
                                        "route_reflector_client": {"type": "bool", "default": None},
                                        "send_community": {
                                            "type": "str",
                                            "choices": ["all", "both", "extended", "large", "standard"]
                                        },
                                    },
                                    "type": "dict"
                                },
                                "network": {"type": "list", "default": []},
                                "redistribute": {"type": "list", "default": []},
                                "max_path": {"type": "str", "default": ""},
                                "advertise_all_vni": {"type": "bool", "default": None}
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
