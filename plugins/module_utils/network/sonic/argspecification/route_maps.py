"""
The arg spec for the sonic_bgp_neighbors module
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class BGPProtocolArgs(object):
    def __init__(self, **kwargs):
        pass

    argument_spec = {
        'config': {
            'elements': 'dict',
            'options': {
                'map_name': {'required': True, 'type': 'str'},
                'action': {
                    'choices': ['permit', 'deny'],
                    'type': 'str'
                },
                'sequence_num': {
                    'type': 'int'
                },
                'on_match': {'type': 'bool'},  # implemetion in progress
                'description': {'type': 'str'},  # implemetion in progress
                'match': {  # implemetion in progress
                    'options': {
                        'access_path_list_name': {'type': 'str'},
                        'community': {
                            'options': {
                                "community_num": {'type': 'int'},
                                "comm_list_name": {'type': 'str'},
                                "exact_match": {'type': 'bool'},
                            },
                            'type': 'dict'
                        },
                        'interface': {'type': 'str'},
                        'ipv4': {
                            'options': {
                                'prefix_list': {'type': 'str'},
                            },
                            'type': 'dict'
                        },
                        'ipv6': {
                            'options': {
                                'prefix_list': {'type': 'str'},
                            },
                            'type': 'dict'
                        },
                        'source_protocol': {
                            'choices': ['bgp', 'connected'],
                            'type': 'str'
                        },
                    },
                    'type': 'dict'
                },
                'set': {
                    'options': {
                        'ip': {'type': 'str'},
                        'ipv6_next_hop': {  # implemetion in progress
                            'options': {
                                'prefer_global': {'type': 'bool'}
                            },
                            'type': 'dict'
                        },
                        'origin': {  # implemetion in progress
                            'options': {
                                'egp': {'type': 'bool'},
                                'igp': {'type': 'bool'},
                                'incomplete': {'type': 'bool'},
                            },
                            'type': 'dict'
                        },
                        'community': {  # implemetion in progress
                            'options': {
                                'community_number': {
                                    'elements': 'str',
                                    'type': 'list'
                                },
                                'community_attributes': {
                                    'elements': 'str',
                                    'type': 'list',
                                    'mutually_exclusive': [
                                        ['none', 'local_as'],
                                        ['none', 'no_advertise'],
                                        ['none', 'no_export'],
                                        ['none', 'no_peer'],
                                        ['none', 'additive']
                                    ],
                                    'choices': [
                                        'local_as',
                                        'no_advertise',
                                        'no_export',
                                        'no_peer',
                                        'additive',
                                        'none'
                                    ]
                                },
                            },
                            'type': 'dict'
                        },
                    },
                    'type': 'dict'
                },
            },
            'type': 'list'
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
    }  # pylint: disable=C0301
