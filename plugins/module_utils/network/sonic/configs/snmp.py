from __future__ import absolute_import, division, print_function
from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.configs.sonic_config.sonic_config import \
    SonicConfig
from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.utils.utils import (
    get_substring_starstwith_matched_item_list)


class SNMPConfig(object):

    def __init__(self) -> None:
        self.running_config = {}
        self.diff = None

    def delete_config(self, module):
        commands = []
        running_config = list(self.running_config.keys())
        module_config = module.params['config']
        agent_module_config = module_config["agent"]
        trap_module_config = module_config["trap"]
        # contact_module_config = module_config["contact"]
        # location_module_config = module_config["location"]
        # community_module_config = module_config["community"]
        if agent_module_config and (agent_module_config['ipv4'] or agent_module_config['ipv6']):
            ip = agent_module_config['ipv4'] if module_config['ipv4'] else module_config['ipv6']
            key = (f"snmp-server agent add {ip} port {agent_module_config.get('port', 22)} "
                   f"vrf {agent_module_config.get('vrf_name')}")
            if key in running_config:
                commands.extend(["config", f"no {key}", "end", "save"])
                self.diff["snmp_server"].append(f"- {key}")

        if trap_module_config and (trap_module_config['ipv4'] or agent_module_config['ipv6']):
            ip = trap_module_config['ipv4'] if trap_module_config['ipv4'] else trap_module_config['ipv6']
            key = (f"snmp-server trap modify {trap_module_config['modify_version']} {ip} port "
                   f"{trap_module_config.get('port', 22)} vrf {trap_module_config.get('vrf_name')} "
                   f"community {trap_module_config['community']}")
            if key in running_config:
                commands.extend(["config", f"no {key}", "end", "save"])
                self.diff["snmp_server"].append(f"- {key}")
        return commands

    def merge_config(self, module):
        commands = []
        running_config = list(self.running_config.keys())
        module_config = module.params['config']
        agent_module_config = module_config["agent"]  # default None
        trap_module_config = module_config["trap"]  # default None
        contact_module_config = module_config["contact"]  # default None
        location_module_config = module_config["location"]  # default None
        community_module_config = module_config["community"]  # default None

        if agent_module_config and (agent_module_config['ipv4'] or agent_module_config['ipv6']):
            self.diff["snmp_server"].append(f"+ {trap_module_config}")
            ip = agent_module_config['ipv4'] if agent_module_config['ipv4'] else agent_module_config['ipv6']
            key = (f"snmp-server agent add {ip} port {agent_module_config.get('port', 22)} vrf "
                   f"{agent_module_config.get('vrf_name')}")
            configured_snmp = get_substring_starstwith_matched_item_list("snmp-server agent", running_config)
            if not configured_snmp:
                commands.extend(["config", key, "end", "save"])
                self.diff["snmp_server"].append(f"+ {key}")
            elif key != configured_snmp:
                commands.extend(["config", f"no {configured_snmp}", key, "end", "save"])
                self.diff["snmp_server"].append(f"- {configured_snmp}")
                self.diff["snmp_server"].append(f"+ {key}")

        if trap_module_config and (trap_module_config['ipv4'] or trap_module_config['ipv6']):
            self.diff["snmp_server"].append(f"+ {trap_module_config}")
            ip = trap_module_config['ipv4'] if trap_module_config['ipv4'] else trap_module_config['ipv6']
            self.diff["snmp_server"].append(f"+ {ip}")
            # snmp-server trap modify {} 127.0.0.1  port 49  vrf  Vrf2 community Public
            key = (f"snmp-server trap modify {trap_module_config['modify_version']} {ip} "
                   f"port {trap_module_config.get('port', 22)} vrf {trap_module_config.get('vrf_name')} "
                   f"community {trap_module_config['community']}")
            self.diff["snmp_server"].append(f"+ {key}")
            configured_snmp = get_substring_starstwith_matched_item_list("snmp-server trap", running_config)
            if not configured_snmp:
                commands.extend(["config", key, "end", "save"])
                self.diff["snmp_server"].append(f"+ {key}")
            elif key != configured_snmp:
                commands.extend(["config", f"no {configured_snmp}", key, "end", "save"])
                self.diff["snmp_server"].append(f"- {configured_snmp}")
                self.diff["snmp_server"].append(f"+ {key}")
        return commands

    def get_config_commands(self, module, get_current_config=True):
        commands = list()
        # self.diff = True
        self.diff = {"snmp_server": []}
        # if get_current_config:
        self.running_config = SonicConfig().get_running_configs(module)["snmp_server"]
        if module.params['state'] == "delete":
            commands.extend(self.delete_config(module))
        else:
            commands.extend(self.merge_config(module))

        return commands, self.diff
