from __future__ import absolute_import, division, print_function
from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.configs.sonic_config.sonic_config import \
    SonicConfig
from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.utils.utils import (
    get_substring_starstwith_matched_item_list,
    substring_starstwith_check)
from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.utils.interfaces_util import (
    config_mtu,
    config_description,
    config_autoneg,
    config_fec,
    config_ip_address,
    config_speed)


class InterfaceConfig(object):

    def __init__(self) -> None:
        self.running_config = {}
        self.diff = None

    def delete_config(self, module):
        commands = []

        module_config_list = module.params['config']
        delete_configs = ['interfaces', 'enable', 'autoneg', 'mtu', 'speed', 'description', 'fec', 'ip_address']
        for module_config in module_config_list:
            filtered_module_config = {key: value for key, value in module_config.items() if
                                      value is not None and value not in ('', [])}
            delete_interface = [item for item in list(filtered_module_config.keys()) if item in delete_configs]
            for config_interface in module_config['interfaces']:
                key = f"interface ethernet {config_interface}"
                self.diff["interfaces"][key] = self.diff["interfaces"].get(key, [])
                if key in self.running_config:
                    config_items = self.running_config.get(key, [])
                    commands.append(f"config terminal")
                    if len(delete_interface) == 1:
                        reverse_config_items = config_items[::-1]
                        if reverse_config_items:
                            commands.append(f"interface ethernet {config_interface}")
                            for item in reverse_config_items:
                                if "shutdown" in item:
                                    commands.append(f"shutdown")
                                    self.diff["interfaces"][key].append("- no shutdown")
                                else:
                                    commands.append(f"no {item}")
                                    self.diff["interfaces"][key].append(f"- {item}")
                            commands.append(f"exit")
                        commands.append(f"no interface ethernet {config_interface}")
                    else:
                        config_list = self.running_config[key]
                        commands.append(f"interface ethernet {config_interface}")
                        if module_config['enable'] or module_config['enable'] is False:
                            if "shutdown" in config_list or "no shutdown" in config_list:
                                commands.append(f"shutdown")
                                self.diff["interfaces"][key].append(f"+ shutdown")
                        if module_config['ip_address']:
                            cmd = f"ip address {'ip_address'}"
                            if cmd in config_list:
                                commands.append(f"no {cmd}")
                                self.diff["interfaces"][key].append(f"- {cmd}")
                        if module_config['autoneg']:
                            if "autoneg enable" in config_list:
                                commands.append(f"no autoneg enable")
                                self.diff["interfaces"][key].append(f"- autoneg enable")
                        if module_config['mtu']:
                            if f"mtu {module_config['mtu']}" in config_list:
                                commands.append(f"no mtu {module_config['mtu']}")
                                self.diff["interfaces"][key].append(f"- mtu {module_config['mtu']}")
                        if module_config['speed']:
                            if f"speed {module_config['speed']}" in config_list:
                                commands.append(f"no speed {module_config['speed']}")
                                self.diff["interfaces"][key].append(f"- speed {module_config['speed']}")
                        if module_config['description']:
                            if f"description {module_config['description']}" in config_list:
                                commands.append(f"no description {module_config['description']}")
                                self.diff["interfaces"][key].append(f"- description {module_config['description']}")
                        if module_config['fec']:
                            if "fec {module_config['fec']}" in config_list:
                                commands.append(f"no forward-error-correction {module_config['fec']}")
                                self.diff["interfaces"][key].append(f"- forward-error-correction {module_config['fec']}"
                                                                    )
                    commands.extend(['end', 'save'])
        return commands

    def merge_config(self, module):
        commands = []
        module_config_list = module.params['config']
        for module_config in module_config_list:
            for config_interface in module_config['interfaces']:
                key = f"interface ethernet {config_interface}"
                self.diff["interfaces"][key] = self.diff["interfaces"].get(key, [])
                init_config_cmds = ['config terminal', key]
                commands.extend(init_config_cmds)
                config_list = self.running_config.get(key, [])

                if module_config['enable'] is False:
                    if not substring_starstwith_check("shutdown", config_list):
                        commands.append(f"shutdown")
                        self.diff["interfaces"][key].append(f"+ shutdown")
                elif module_config['enable'] is True:
                    if substring_starstwith_check("shutdown", config_list):
                        commands.append(f"no shutdown")
                        self.diff["interfaces"][key].append(f"- shutdown")
                        self.diff["interfaces"][key].append(f"+ no shutdown")

                if module_config['ip_address']:
                    cmds, self.diff = config_ip_address(module_config, config_list, diff=self.diff, key=key)
                    commands.extend(cmds)
                if module_config['autoneg']:
                    cmds, self.diff = config_autoneg(module_config, config_list, diff=self.diff, key=key)
                    commands.extend(cmds)
                if module_config['mtu']:
                    cmds, self.diff = config_mtu(module_config, config_list, diff=self.diff, key=key)
                    commands.extend(cmds)
                if module_config['speed']:
                    cmds, self.diff = config_speed(module_config, config_list, diff=self.diff, key=key)
                    commands.extend(cmds)
                if module_config['description']:
                    cmds, self.diff = config_description(module_config, config_list, diff=self.diff, key=key)
                    commands.extend(cmds)
                if module_config['fec']:
                    cmds, self.diff = config_fec(module_config, config_list, diff=self.diff, key=key)
                    commands.extend(cmds)

                commands.extend(['end', 'save'])
        return commands

    def get_config_commands(self, module, get_current_config=True):
        commands = list()
        # self.diff = True
        self.diff = {"interfaces": {}}
        # if get_current_config:
        self.running_config = SonicConfig().get_running_configs(module)
        self.running_config = self.running_config["interfaces"]
        if module.params['state'] == "delete":
            commands.extend(self.delete_config(module))
        else:
            commands.extend(self.merge_config(module))

        return commands, self.diff
