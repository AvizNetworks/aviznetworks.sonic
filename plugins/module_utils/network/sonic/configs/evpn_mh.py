from __future__ import absolute_import, division, print_function
from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.configs.sonic_config.sonic_config import \
    SonicConfig
from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.utils.utils import (
    get_substring_starstwith_matched_item_list,
    substring_starstwith_check)

class EvpnMHConfig(object):

    def __init__(self) -> None:
        self.running_interfaces_conf = None
        self.running_mlag_conf = None
        self.running_conf = None
        self.diff = None

    def delete_config(self, module):
        commands = []
        module_config_list = module.params['config']
        for module_config in module_config_list:
            pch_id = ""
            if module_config['interface'] and "ethernet" not in module_config['interface'].lower():
                pch_id = "".join([c for c in str(module_config['interface']) if c.isdigit()])
            if module_config['es_id'] and module_config['es_sys_mac'] and pch_id:
                key = f"interface port-channel {pch_id}"
                self.diff["interfaces"][key] = []
                evpn_mh = f"evpn-mh es-id {module_config['es_id']} es-sys-mac {module_config['es_sys_mac']}"
                config_list_pch = self.running_interfaces_conf.get(key, [])
                mvpn_mh_running_conf = get_substring_starstwith_matched_item_list("evpn-mh", config_list_pch)
                if mvpn_mh_running_conf and evpn_mh == mvpn_mh_running_conf:
                    commands.extend(["config", key, f"no {mvpn_mh_running_conf}", "end", "save"])
                    self.diff["interfaces"][key].append(f"- {mvpn_mh_running_conf}")
            elif module_config['uplink'] and module_config['interface'] and "ethernet" in module_config['interface'].lower():
                key = f"interface ethernet {module_config['interface']}"
                self.diff["interfaces"][key] = []
                evpn_mh = f"evpn-mh uplink"
                config_list_pch = self.running_interfaces_conf.get(key, [])
                mvpn_mh_running_conf = get_substring_starstwith_matched_item_list(evpn_mh, config_list_pch)
                if mvpn_mh_running_conf:
                    commands.extend(["config", key, f"no {evpn_mh}", "end", "save"])
                    self.diff["interfaces"][key].append(f"- {evpn_mh}")
        return commands

    def config_evpn_mh(self, module):
        commands = []
        module_config_list = module.params['config']
        for module_config in module_config_list:
            pch_id = ""
            if module_config['interface'] and "ethernet" not in module_config['interface'].lower():
                pch_id = "".join([c for c in str(module_config['interface']) if c.isdigit()])
            if module_config['es_id'] and module_config['es_sys_mac'] and pch_id:
                key = f"interface port-channel {pch_id}"
                self.diff["interfaces"][key] = []
                evpn_mh = f"evpn-mh es-id {module_config['es_id']} es-sys-mac {module_config['es_sys_mac']}"
                config_list_pch = self.running_interfaces_conf.get(key, [])
                mvpn_mh_running_conf = get_substring_starstwith_matched_item_list("evpn-mh", config_list_pch)
                if evpn_mh != mvpn_mh_running_conf:
                    commands.extend(["config", key])
                    if mvpn_mh_running_conf:
                        self.diff["interfaces"][key].append(f"- {mvpn_mh_running_conf}")
                        commands.append(f"no {mvpn_mh_running_conf}")
                    self.diff["interfaces"][key].append(f"+ {evpn_mh}")
                    commands.extend([evpn_mh, "end", "save"])
            elif module_config['uplink'] and module_config['interface'] and "ethernet" in module_config['interface'].lower():
                key = f"interface ethernet {module_config['interface']}"
                self.diff["interfaces"][key] = []
                evpn_mh = f"evpn-mh uplink"
                config_list_pch = self.running_interfaces_conf.get(key, [])
                mvpn_mh_running_conf = get_substring_starstwith_matched_item_list("evpn-mh uplink", config_list_pch)
                if not mvpn_mh_running_conf:
                    commands.extend(["config", key, evpn_mh, "end", "save"])
                    self.diff["interfaces"][key].append(f"+ {evpn_mh}")
            elif module_config['uplink'] is False and module_config['interface'] and "ethernet" in module_config['interface'].lower():
                key = f"interface ethernet {module_config['interface']}"
                self.diff["interfaces"][key] = []
                evpn_mh = f"evpn-mh uplink"
                config_list_pch = self.running_interfaces_conf.get(key, [])
                mvpn_mh_running_conf = get_substring_starstwith_matched_item_list("evpn-mh uplink", config_list_pch)
                if mvpn_mh_running_conf:
                    commands.extend(["config", key, f"no {evpn_mh}", "end", "save"])
                    self.diff["interfaces"][key].append(f"- {evpn_mh}")
        return commands

    def get_config_commands(self, module, get_current_config=True):
        commands = list()
        self.diff = {"interfaces": {}}
        if get_current_config:
            self.running_conf = SonicConfig().get_running_configs(module)
            self.running_mlag_conf = self.running_conf["mlag"]
            self.running_interfaces_conf = self.running_conf["interfaces"]
        if module.params['state'] in ["delete"]:
            commands.extend(self.delete_config(module))

        else:
            commands.extend(self.config_evpn_mh(module))

        return commands, self.diff
