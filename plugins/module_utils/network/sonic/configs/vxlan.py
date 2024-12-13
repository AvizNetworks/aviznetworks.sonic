from __future__ import absolute_import, division, print_function
from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.configs.sonic_config.sonic_config import (
    SonicConfig)
from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.utils.utils import (
    get_substring_starstwith_matched_item_list,
    get_list_substring_starstwith_matched_item_list)
from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.utils.vlan_util import (
    config_vlans)


class VxlanConfig(object):

    def __init__(self) -> None:
        self.running_config = {}
        self.running_config_vxlan = {}
        self.diff = None

    def delete_config(self, module):
        commands = []

        module_config_list = module.params['config']
        delete_configs = ['vtep_device', 'loopback_ip', 'evpn_nvo', 'map_vni']
        for module_config in module_config_list:
            filtered_module_config = {}
            for dkey, value in module_config.items():
                if dkey == "map_vni" and module_config["map_vni"]:
                    filtered_module_config["map_vni"] = []
                    for v in value:
                        if v["vlan_id"] and v["vni_id"]:
                            filtered_module_config["map_vni"].append(f'map vlan {v["vlan_id"]} vni {v["vni_id"]}')
                elif value:
                    filtered_module_config[dkey] = value

            # filtered_module_config = {key: value for key, value in module_config.items() if value != ""}
            delete_vxlan = [item for item in list(filtered_module_config.keys()) if item in delete_configs]

            key = f"vxlan {module_config['vtep_device']}"
            self.diff["vxlan"][key] = self.diff["vxlan"].get(key, [])
            if key in self.running_config_vxlan:
                config_items = self.running_config_vxlan.get(key, [])
                commands.append(f"config terminal")
                if len(delete_vxlan) == 1:
                    self.diff["test"] = delete_vxlan
                    reverse_config_items = config_items[::-1]
                    self.diff["reverse_config_items"] = reverse_config_items
                    if reverse_config_items:
                        commands.append(key)
                        for item in reverse_config_items:
                            commands.append(f"no {item}")
                            self.diff["vxlan"][key].append(f"- {item}")
                        commands.append(f"exit")

                    commands.append(f"no {key}")
                    commands.extend(['end', 'save'])
                    self.diff["vxlan"][key].append(f"- {key}")
                else:
                    commands.append(key)
                    flag = True
                    if filtered_module_config["map_vni"]:
                        for item in filtered_module_config["map_vni"]:
                            if item in config_items:
                                flag = False
                                commands.append(f"no {item}")
                                self.diff["vxlan"][key].append(f"- {item}")

                    if module_config['evpn_nvo']:
                        cmd = f"evpn_nvo {module_config['evpn_nvo']}"
                        if cmd in config_items:
                            flag = False
                            commands.append(f"no {cmd}")
                            self.diff["vxlan"][key].append(f"- {cmd}")

                    if module_config['loopback_ip']:
                        cmd = f"loopback-ip {module_config['loopback_ip']}"
                        if cmd in config_items:
                            flag = False
                            commands.append(f"no {cmd}")
                            self.diff["vxlan"][key].append(f"- {cmd}")
                    if flag:
                        commands = commands[:-2]
                    else:
                        commands.extend(['end', 'save'])
        return commands

    def config_loopback(self, module_config, key, config_list):
        commands = []
        if module_config["loopback_ip"]:
            loopback = f"loopback-ip {module_config['loopback_ip']}"
            loopback_str = get_substring_starstwith_matched_item_list("loopback-ip", config_list)
            if loopback_str and loopback_str != loopback:
                commands.append(f"no {loopback_str}")
                self.diff["vxlan"][key].append(f"- {loopback_str}")
                commands.append(loopback)
                self.diff["vxlan"][key].append(f"+ {loopback}")
            elif not loopback_str:
                commands.append(loopback)
                self.diff["vxlan"][key].append(f"+ {loopback}")
        return commands

    def config_evpn_nvo(self, module_config, key, config_list):
        commands = []
        if module_config["evpn_nvo"]:
            evpn = f"evpn_nvo {module_config['evpn_nvo']}"
            evpn_str = get_substring_starstwith_matched_item_list("evpn_nvo", config_list)
            if evpn_str and evpn_str != evpn:
                commands.append(f"no {evpn_str}")
                self.diff["vxlan"][key].append(f"- {evpn_str}")
                commands.append(evpn)
                self.diff["vxlan"][key].append(f"+ {evpn}")
            elif not evpn_str:
                commands.append(evpn)
                self.diff["vxlan"][key].append(f"+ {evpn}")
        return commands

    def config_map_vni(self, module_config, key, config_list):
        commands = []
        map_vni_str = get_list_substring_starstwith_matched_item_list("map vlan", config_list)
        for map_vni in module_config["map_vni"]:
            if map_vni['vlan_id'] and map_vni['vni_id']:
                map_key = f"map vlan {map_vni['vlan_id']} vni {map_vni['vni_id']}"
                if map_key not in map_vni_str:
                    commands.append(map_key)
                    self.diff["vxlan"][key].append(f"+ {map_key}")
        return commands

    def merge_config(self, module):
        commands = []
        module_config_list = module.params['config']
        for module_config in module_config_list:
            # create VLANs
            for map_vni in module_config["map_vni"]:
                if map_vni['vlan_id'] and map_vni['vni_id']:
                    cmds, self.diff = config_vlans(map_vni, config_list=self.running_config, diff=self.diff)
                    commands.extend(cmds)
            vtap = module_config.get("vtep_device")
            key = f"vxlan {vtap}"
            self.diff["vxlan"][key] = self.diff["vxlan"].get(key, [])
            commands.extend(['config terminal', key])

            config_list = self.running_config_vxlan.get(key, [])
            cmds = self.config_loopback(module_config, key, config_list)
            commands.extend(cmds)

            cmds = self.config_evpn_nvo(module_config, key, config_list)
            commands.extend(cmds)

            cmds = self.config_map_vni(module_config, key, config_list)
            commands.extend(cmds)

            commands.extend(['end', 'save'])
        return commands

    def get_config_commands(self, module, get_current_config=True):
        commands = list()
        self.diff = {"vxlan": {}, "vlan": {}}
        # if get_current_config:
        self.running_config = SonicConfig().get_running_configs(module)
        self.running_config_vxlan = self.running_config["vxlan"]
        if module.params['state'] == "delete":
            commands.extend(self.delete_config(module))
        else:
            commands.extend(self.merge_config(module))

        return commands, self.diff
