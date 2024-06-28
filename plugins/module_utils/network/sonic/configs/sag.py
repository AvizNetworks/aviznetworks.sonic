from __future__ import absolute_import, division, print_function
from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.configs.sonic_config.sonic_config import \
    SonicConfig
from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.utils.utils import (
    get_substring_starstwith_matched_item_list)


class SAGConfig(object):

    def __init__(self) -> None:
        self.running_config = {}
        self.diff = None

    def delete_config(self, module):
        commands = []
        flag = True
        module_config = module.params.get('config', {})
        if module_config is None:
            module_config = {}
        delete_configs = ['mac_address', 'enable_ipv4', 'enable_ipv6']
        filtered_module_config = {key: value for key, value in module_config.items() if
                                  value is not None and value != ""}
        delete_sag = [item for item in list(filtered_module_config.keys()) if item in delete_configs]
        commands.extend(['config terminal', "sag"])
        self.diff["sag"] = self.diff.get("sag", [])
        config_list = self.running_config.get("sag", [])
        if len(delete_sag) == 0:
            flag = False
            reverse_config_items = config_list[::-1]
            for item in reverse_config_items:
                commands.append(f"no {item}")
                self.diff["sag"].append(f"- {item}")
            self.diff["sag"].append(f"- sag")
            commands.extend(["exit", "no sag"])
        else:
            if module_config['mac_address']:
                key = f"anycast-gateway-mac {module_config['mac_address']}"
                mac_add = get_substring_starstwith_matched_item_list("anycast-gateway-mac", config_list)
                if mac_add == key:
                    flag = False
                    commands.append(f"no {key}")
                    self.diff["sag"].append(f"- {key}")

            if module_config['mac_address'] and module_config['enable_ipv4']:
                key = f"enable ip"
                ipv4_enable = get_substring_starstwith_matched_item_list(key, config_list)
                if ipv4_enable and ipv4_enable == key:
                    flag = False
                    commands.append(f"no {key}")
                    self.diff["sag"].append(f"- {key}")

            if module_config['mac_address'] and module_config['enable_ipv6']:
                key = f"enable ipv6"
                ipv6_enable = get_substring_starstwith_matched_item_list(key, config_list)
                if not ipv6_enable:
                    flag = False
                    commands.append(f"no {key}")
                    self.diff["sag"].append(f"- {key}")
        if flag:
            commands = commands[:-2]
        else:
            commands.extend(['end', 'save'])

        return commands

    def merge_config(self, module):
        commands = []
        module_config = module.params['config']
        commands.extend(['config terminal', "sag"])
        self.diff["sag"] = self.diff.get("sag", [])
        config_list = self.running_config.get("sag", [])
        flag = True
        if module_config['mac_address']:
            key = f"anycast-gateway-mac {module_config['mac_address']}"
            mac_add = get_substring_starstwith_matched_item_list("anycast-gateway-mac", config_list)
            if mac_add != key:
                flag = False
                commands.append(key)  # it will override the old mac address
                if mac_add:
                    self.diff["sag"].append(f"- {mac_add}")
                self.diff["sag"].append(f"+ {key}")

        if module_config['mac_address'] and module_config['enable_ipv4']:
            key = f"enable ip"
            ipv4_enable = get_substring_starstwith_matched_item_list(key, config_list)
            if not ipv4_enable or ipv4_enable != key:
                flag = False
                commands.append(key)
                self.diff["sag"].append(f"+ {key}")

        elif module_config['mac_address'] and module_config['enable_ipv4'] is False:
            key = f"enable ip"
            ipv4_enable = get_substring_starstwith_matched_item_list(key, config_list)
            if ipv4_enable:
                flag = False
                commands.append(f"no {key}")
                self.diff["sag"].append(f"- {key}")

        if module_config['mac_address'] and module_config['enable_ipv6']:
            key = f"enable ipv6"
            ipv6_enable = get_substring_starstwith_matched_item_list(key, self.running_config)
            if not ipv6_enable:
                flag = False
                commands.append(key)
                self.diff["sag"].append(f"+ {key}")
        elif module_config['mac_address'] and module_config['enable_ipv6'] is False:
            key = f"enable ipv6"
            ipv6_enable = get_substring_starstwith_matched_item_list(key, self.running_config)
            if ipv6_enable:
                flag = False
                commands.append(f"no {key}")
                self.diff["sag"].append(f"- {key}")

        if flag:
            commands = commands[:-2]
        else:
            commands.extend(['end', 'save'])

        return commands

    def get_config_commands(self, module, get_current_config=True):
        commands = list()
        # self.diff = True
        self.diff = {"sag": []}
        # if get_current_config:
        self.running_config = SonicConfig().get_running_configs(module)
        self.running_config = self.running_config["sag"]
        if module.params['state'] == "delete":
            commands.extend(self.delete_config(module))
        else:
            commands.extend(self.merge_config(module))

        return commands, self.diff
