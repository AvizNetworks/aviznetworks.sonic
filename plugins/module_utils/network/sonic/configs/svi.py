from __future__ import absolute_import, division, print_function
from ansible_collections.aviznetworks.sonic_fmcli.plugins.module_utils.network.sonic.configs.sonic_config.sonic_config import \
    SonicConfig
from ansible_collections.aviznetworks.sonic_fmcli.plugins.module_utils.network.sonic.utils.utils import (
    get_substring_starstwith_matched_item_list,
    substring_starstwith_check)
from ansible_collections.aviznetworks.sonic_fmcli.plugins.module_utils.network.sonic.utils.interfaces_util import config_ip_address


class SVIConfig(object):

    def __init__(self) -> None:
        pass

    def delete_config(self, module):
        commands = []

        module_config_list = module.params['config']
        delete_configs = ['vlan_id', 'ip_address']
        for module_config in module_config_list:
            filtered_module_config = {key: value for key, value in module_config.items() if
                                      value is not None and value not in ('', [])}
            delete_vlan = [item for item in list(filtered_module_config.keys()) if item in delete_configs]

            key = f"interface vlan {module_config['vlan_id']}"
            self.diff["interfaces"][key] = []
            if key in self.running_config:
                commands.append(f"config terminal")
                if len(delete_vlan) == 1:
                    commands.append(f"no interface vlan {module_config['vlan_id']}")
                    self.diff["interfaces"][key].append(f"- {key}")
                else:
                    config_list = self.running_config[key]
                    commands.append(key)
                    if module_config['ip_address']:
                        cmd = f"ip address {module_config['ip_address']}"
                        if cmd in config_list:
                            commands.append(f"no {cmd}")
                            self.diff["interfaces"][key].append(f"- {cmd}")

                commands.extend(['end', 'save'])

        return commands

    def replace_config(self, module):
        commands = []
        module_config_list = module.params['config']
        for module_config in module_config_list:
            key = f"interface vlan {module_config['vlan_id']}"
            self.diff["interfaces"][key] = []
            if key in self.running_config:
                config_list = self.running_config.get(key, [])
                if module_config['ip_address']:
                    cmd = f"ip address {module_config['ip_address']}"
                    if cmd in config_list:
                        pass
                    elif substring_starstwith_check("ip address", config_list):
                        commands.append(f"config terminal")
                        commands.append(key)
                        cmd_dlt = get_substring_starstwith_matched_item_list("ip address", config_list)
                        commands.append(f"no {cmd_dlt}")
                        commands.append(cmd)
                        self.diff["interfaces"][key].append(f"- {cmd_dlt}")
                        self.diff["interfaces"][key].append(f"+ {cmd}")
                        commands.extend(['end', 'save'])

        return commands

    def merge_config(self, module):
        commands = []
        module_config_list = module.params['config']
        for module_config in module_config_list:
            key = f"interface vlan {module_config['vlan_id']}"
            self.diff["interfaces"][key] = []
            init_config_cmds = ['config terminal', key]
            commands.extend(init_config_cmds)
            config_list = self.running_config.get(key, [])

            if module_config['ip_address']:
                cmds, self.diff = config_ip_address(module_config, config_list, diff=self.diff, key=key)
                commands.extend(cmds)
            commands.extend(['end', 'save'])
        return commands

    def get_config_commands(self, module, get_current_config=True):
        commands = list()
        # self.diff = True
        self.diff = {"interfaces": {}}
        if get_current_config:
            self.running_config = SonicConfig().get_running_configs(module)["interfaces"]
        # self.running_config = self.running_config
        if module.params['state'] == "delete":
            commands.extend(self.delete_config(module))
        elif module.params['state'] == "replace":
            commands.extend(self.replace_config(module))
        else:
            commands.extend(self.merge_config(module))

        if get_current_config:
            SonicConfig().get_running_configs(module)

        return commands, self.diff
