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
            "elements": "dict",
            "options": {
                "bgp_asn": {"required": True, "type": "str"},
                "neighbor": {
                    "options": {
                        "interface": { # implemetion in progress
                            "options": {
                                "interface": {"type": "str"}, 
                                "description": {"type": "str"},
                                "peer_group_name": {"type": "str"},
                                "remote_as": {
                                    "options": {
                                        "as_number" :{"type": "int"},
                                        "external" :{"type": "bool", "default": None},
                                        "internal" :{"type": "bool", "default": None},
                                    },
                                    "required_one_of": [["as_number", "external", "internal"]],
                                    "type": "dict"
                                },
                                "shutdown": {"type": "bool", "default": None},
                            },
                            "type": "dict"
                        },
                        "ipv4": {
                            "options": {
                                "ip": {"type": "list", "default": []},
                                "remote_as": {"type": "str","default": ""},
                                "extended_nexthop": {"type": "bool", "default": False},
                                "description": {"type": "str"}, # implemetion in progress
                                "peer_group_name": {"type": "str"}, # implemetion in progress
                                "bfd": {"type": "str"}, # implemetion in progress
                                "shoutdown": {"type": "bool", "default": False}, # implemetion in progress
                                "timers": { # implemetion in progress
                                    "options": {
                                        "keepalive": {"type": "int"}
                                    },
                                    "type": "dict"
                                },
                                "update_source": { # implemetion in progress
                                    "options": {
                                        "interface": {"type": "str"},
                                        "portchannel": {"type": "str"}
                                    },
                                    "required_one_of": [["interface", "portchannel"]],
                                    "type": "dict"
                                }                                   
                            },
                            "type": "dict"
                        },
                        "ipv6":{ # implemetion in progress
                            "options": {
                                "ip": {"type": "list"},
                                "remote_as": {"type": "str"},
                                "extended_nexthop": {"type": "bool", "default": None},
                                "description": {"type": "str"}, # implemetion in progress
                                "peer_group_name": {"type": "str"}, # implemetion in progress
                                "bfd": {"type": "str"}, # implemetion in progress
                                "shoutdown": {"type": "bool", "default": None}, # implemetion in progress
                                "timers": { # implemetion in progress
                                    "options": {
                                        "keepalive": {"type": "int"}
                                    },
                                    "type": "dict"
                                },
                                "update_source": { # implemetion in progress
                                    "options": {
                                        "interface": {"type": "str"},
                                        "portchannel": {"type": "str"}
                                    },
                                    "required_one_of": [["interface", "portchannel"]],
                                    "type": "dict"
                                }                                   
                            },
                            "type": "dict"
                        },
                        "Peer_group_Name":{ # implemetion in progress
                            "options": {
                                "peer_group_name": {"type": "str"},
                                "extended_nexthop": {"type": "bool", "default": None}, 
                                "description": {"type": "str"},
                                "peer_group": {"type": "bool", "default": None},
                                "remote_as": {
                                    "options": {
                                        "as_number" :{"type": "int"},
                                        "external" :{"type": "bool", "default": None},
                                        "internal" :{"type": "bool", "default": None},
                                    },
                                    "required_one_of": [["as_number", "external", "internal"]],
                                    "type": "dict"
                                },
                                "shutdown": {"type": "bool", "default": None},
                                "timers": {
                                    "options": {
                                        "keepalive": {"type": "int"}
                                    },
                                    "type": "dict"
                                }
                            },
                            "type": "dict"
                        },
                    },
                    "type": "dict"
                },
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
        "commands": {"elements": "str" , "type": "list"},
        "diff": {"elements": "str" , "type": "list"}
    }


  