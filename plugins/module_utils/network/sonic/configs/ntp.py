from __future__ import absolute_import, division, print_function
from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.configs.sonic_config.sonic_config import \
    SonicConfig
from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.utils.utils import (
    get_substring_starstwith_matched_item_list)


class NTPConfig(object):

    def __init__(self) -> None:
        self.running_config = {}
        self.diff = None

    def delete_config(self, module):
        commands = []
        module_config = module.params['config']
        if module_config['ipv4'] or module_config['ipv6']:
            key = f"ntp add {module_config['ipv4']}" if module_config['ipv4'] else f"ntp add {module_config['ipv6']}"
            if key in self.running_config:
                commands.extend(["config", f"no {key}", "end", "save"])
                self.diff["common_config"].append(f"- {key}")

        if module_config['timezone']:
            key = f"clock timezone {module_config['timezone']}"
            if key in self.running_config:
                commands.extend(["config", f"no {key}", "end", "save"])
                self.diff["common_config"].append(f"- {key}")
        return commands

    def merge_config(self, module):
        commands = []
        module_config = module.params['config']
        if module_config['ipv4'] or module_config['ipv6']:
            ip = module_config['ipv4'] if module_config['ipv4'] else module_config['ipv6']
            key = f"ntp add {ip}"
            configured_ntp = get_substring_starstwith_matched_item_list("ntp add", list(self.running_config.keys()))
            if not configured_ntp:
                commands.extend(["config", key, "end", "save"])
                self.diff["common_config"].append(f"+ {key}")
            elif key != configured_ntp:
                commands.extend(["config", f"no {configured_ntp}", key, "end", "save"])
                self.diff["common_config"].append(f"- {configured_ntp}")
                self.diff["common_config"].append(f"+ {key}")

        if module_config['timezone']:
            key = f"clock timezone {module_config['timezone']}"
            configured_timezone = get_substring_starstwith_matched_item_list("clock timezone",
                                                                             list(self.running_config.keys()))
            if not configured_timezone:
                commands.extend(["config", key, "end", "save"])
                self.diff["common_config"].append(f"+ {key}")
            elif key != configured_timezone:
                commands.extend(["config", f"no {configured_timezone}", key, "end", "save"])
                self.diff["common_config"].append(f"- {configured_timezone}")
                self.diff["common_config"].append(f"+ {key}")
        return commands

    def get_config_commands(self, module, get_current_config=True):
        commands = list()
        # self.diff = True
        self.diff = {"common_config": []}
        # if get_current_config:
        self.running_config = SonicConfig().get_running_configs(module)
        if module.params['state'] == "delete":
            commands.extend(self.delete_config(module))
        else:
            commands.extend(self.merge_config(module))

        return commands, self.diff
