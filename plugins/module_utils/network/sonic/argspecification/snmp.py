from __future__ import absolute_import, division, print_function

__metaclass__ = type


class SNMPArgs(object):
    """The arg spec for the sonic_interfaces module
    """

    def __init__(self, **kwargs):
        pass

    argument_spec = {
        "config": {
            "options": {
                "agent": { #snmp-server agent add <ip4addr | ip6addr > [port <value>] [vrf  <value>]
                            "options": {
                                "ipv4": {"type": "str", "default": ""},
                                "ipv6": {"type": "str", "default": ""},
                                "port": {"type": "int", "default": 0},
                                "vrf_name": {"type": "str","default": "None"}
                            },
                            "type": "dict"
                },
                "trap": { # snmp-server  trap modify <version> <ip4addr|ip6addr> [port <value>] [vrf <value>] [community <value>]
                            "options": {
                                "modify_version": {"type": "str", "default": ""},
                                "ipv4": {"type": "str", "default": ""},
                                "ipv6": {"type": "str", "default": ""},
                                "port": {"type": "int", "default": 0},
                                "vrf_name": {"type": "str","default": "None"},
                                "community": {"type": "str","default": "None"}
                            },
                            "type": "dict"
                },
                "contact": { # snmp-server contact contact-mail <cont_mail> contact-name <cont_name>
                            "options": { # Ex: snmp-server contact contact-mail admin@aviznetworks.com contact-name Aviz
                                "email": {"type": "str", "default": ""},
                                "name": {"type": "str", "default": ""},
                            },
                            "type": "dict"
                },
                "location": { # snmp-server location <location>
                            "options": { # Ex: snmp-server location Aviz Networks, Gachibowli, Hyderabad - 500032
                                "location": {"type": "str", "default": ""}
                            },
                            "type": "dict"
                }
                ,
                "community": { # snmp-server  community <comm> (RO | RW)
                            "options": { # snmp-server community avizCommunity RO
                                "name": {"type": "str", "default": ""},
                                "access": {"type": "str", "choices": ["RO", "RW"], "default": "RO"}
                            }, # RO -> Read Only access | RW -> Read and Write access
                            "type": "dict"
                }
            },
            "type": "dict"
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
