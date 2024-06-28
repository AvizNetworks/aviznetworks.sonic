from __future__ import absolute_import, division, print_function
from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.configs.sonic_config.sonic_config import \
    SonicConfig
from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.utils.utils import (
    get_substring_starstwith_matched_item_list,
    get_list_substring_starstwith_matched_item_list,
    substring_starstwith_check)
from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.utils.interfaces_util import (
    config_mtu,
    config_description,
    config_autoneg,
    config_fec,
    config_ip_address,
    config_speed)
from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.utils.vlan_util import (
    config_vlans,
    get_vlan_ids,
    config_anycast_gateway
)


class SyslogConfig(object):

    def __init__(self) -> None:
        self.running_config = {}
        self.diff = None

    def delete_config(self, module):
        commands = []
        module_config_list = module.params['config']
        syslog_add = get_list_substring_starstwith_matched_item_list("syslog add ", self.running_config)
        for module_config in module_config_list:
            self.diff["syslog"] = self.diff.get("syslog", [])
            if module_config["ip"]:
                key = f"syslog add {module_config['ip']}"
                if key in syslog_add:
                    commands.extend(['config terminal', f'no {key}', 'end', 'save'])
                    self.diff["syslog"].append(f"- {key}")
            else:
                for item in syslog_add:
                    commands.extend(['config terminal', f'no {item}', 'end', 'save'])
                    self.diff["syslog"].append(f"- {item}")
        return commands

    def merge_config(self, module):
        commands = []
        module_config_list = module.params['config']
        syslog_add = get_list_substring_starstwith_matched_item_list("syslog add ", self.running_config)
        for module_config in module_config_list:
            self.diff["syslog"] = self.diff.get("syslog", [])
            if module_config["ip"]:
                key = f"syslog add {module_config['ip']}"
                if key not in syslog_add:
                    commands.extend(['config terminal', key, 'end', 'save'])
                    self.diff["syslog"].append(f"+ {key}")
        return commands

    def get_config_commands(self, module, get_current_config=True):
        commands = list()
        # self.diff = True
        self.diff = {"syslog": []}
        # if get_current_config:
        self.running_config = SonicConfig().get_running_configs(module)
        if module.params['state'] == "delete":
            commands.extend(self.delete_config(module))
        else:
            commands.extend(self.merge_config(module))

        return commands, self.diff
