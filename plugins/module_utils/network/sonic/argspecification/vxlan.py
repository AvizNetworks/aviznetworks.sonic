from __future__ import absolute_import, division, print_function

__metaclass__ = type


class VxlanArgs(object):
    """The arg spec for the sonic_vxlan module
    """

    def __init__(self, **kwargs):
        pass

    argument_spec = {
        "config": {
            "elements": "dict",
            "options": {
                "vtep_device": {"type": "str", "required": True},  # VxLAN Tunnel Endpoint
                "loopback_ip": {"type": "str", "default": ""},  # 10.4.5.2
                "evpn_nvo": {"type": "str", "default": ""},  # ex: EVPN Network Virtualization overlay, test_lay
                "map_vni": {
                    'options': {
                        'vlan_id': {'type': 'str', "default": ""},
                        'vni_id': {'type': 'str', "default": ""}
                    },
                    'type': 'list'
                }
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
