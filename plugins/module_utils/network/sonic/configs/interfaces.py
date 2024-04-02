from __future__ import absolute_import, division, print_function
from ansible_collections.aviznetworks.sonic_fmcli.plugins.module_utils.network.sonic.configs.sonic_config.sonic_config import \
    SonicConfig
from ansible_collections.aviznetworks.sonic_fmcli.plugins.module_utils.network.sonic.utils.utils import (
    get_substring_starstwith_matched_item_list,
    substring_starstwith_check)
from ansible_collections.aviznetworks.sonic_fmcli.plugins.module_utils.network.sonic.utils.interfaces_util import (
    config_mtu,
    config_description,
    config_autoneg,
    config_fec,
    config_ip_address,
    config_speed)


class InterfaceConfig(object):

    def __init__(self) -> None:
        pass

    def delete_config(self, module):
        commands = []

        module_config_list = module.params['config']
        delete_configs = ['interface', 'enable', 'autoneg', 'mtu', 'speed', 'description', 'fec', 'ip_address']
        for module_config in module_config_list:
            filtered_module_config = {key: value for key, value in module_config.items() if
                                      value is not None and value not in ('', [])}
            delete_interface = [item for item in list(filtered_module_config.keys()) if item in delete_configs]

            for config_interface in module_config['interface']:
                key = f"interface ethernet {config_interface}"
                if key in self.running_config:
                    commands.append(f"config terminal")
                    if len(delete_interface) == 1:
                        commands.append(f"no interface ethernet {config_interface}")
                    else:
                        config_list = self.running_config[key]
                        commands.append(f"interface ethernet {config_interface}")
                        if (module_config['enable'] or module_config['enable'] is False):
                            if "shutdown" in config_list or "no shutdown" in config_list:
                                commands.append(f"no shutdown")
                        if module_config['ip']:
                            cmd = f"ip address {'address'}/{'mask'}"
                            if cmd in config_list:
                                commands.append(f"no {cmd}")
                        if module_config['autoneg']:
                            if "autoneg enable" in config_list:
                                commands.append(f"no autoneg enable")
                        if module_config['mtu']:
                            if f"mtu {module_config['mtu']}" in config_list:
                                commands.append(f"no mtu {module_config['mtu']}")
                        if module_config['speed']:
                            if f"speed {module_config['speed']}" in config_list:
                                commands.append(f"no speed {module_config['speed']}")
                        if module_config['description']:
                            if f"description {module_config['description']}" in config_list:
                                commands.append(f"no description {module_config['description']}")
                        if module_config['fec']:
                            if "fec {module_config['fec']}" in config_list:
                                commands.append(f"no fec {module_config['fec']}")

                    commands.extend(['end', 'save'])

        return commands

    def replace_config(self, module):
        commands = []
        module_config_list = module.params['config']
        delete_configs = ['interface', 'enable', 'autoneg', 'mtu', 'speed', 'description', 'fec', 'ip_address']
        for module_config in module_config_list:
            filtered_module_config = {key: value for key, value in module_config.items() if
                                      value is not None and value not in ('', [])}
            delete_interface = [item for item in list(filtered_module_config.keys()) if item in delete_configs]

            for config_interface in module_config['interface']:
                key = f"interface ethernet {config_interface}"
                if key in self.running_config:
                    commands.append(f"config terminal")
                    commands.append(f"interface ethernet {config_interface}")
                    delete_config_list = self.running_config[key]
                    for item in delete_config_list:
                        commands.append(f"no {item}")
                commands.extend(['end', 'save'])
                commands.extend(self.merge_config(module, module_config_list=[module_config], delete=False))

        return commands

    def merge_config(self, module):
        commands = []
        module_config_list = module.params['config']
        for module_config in module_config_list:
            for config_interface in module_config['interface']:
                key = f"interface ethernet {config_interface}"
                self.diff["interfaces"][key] = []
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
        if get_current_config:
            self.running_config = SonicConfig().get_running_configs(module)
        self.running_config = self.running_config["interfaces"]
        if module.params['state'] == "delete":
            commands.extend(self.delete_config(module))
        elif module.params['state'] == "override":
            commands.extend(self.override_config(module))
        else:
            commands.extend(self.merge_config(module))

        if get_current_config:
            SonicConfig().get_running_configs(module)

        return commands, self.diff
