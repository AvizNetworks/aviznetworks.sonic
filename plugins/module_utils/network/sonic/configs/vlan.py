from __future__ import absolute_import, division, print_function
from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.configs.sonic_config.sonic_config import \
    SonicConfig
from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.utils.utils import (
    get_substring_starstwith_matched_item_list,
    substring_starstwith_check,
    get_list_substring_starstwith_matched_item_list)
from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.utils.interfaces_util import (
    config_mtu,
    config_description,
    config_ip_address,
    config_speed,
    config_channel_group,
    get_portchannel_member_interfaces)
from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.utils.vlan_util import (
    config_vlans,
    get_vlan_ids,
    config_anycast_gateway
)


class VlanConfig(object):

    def __init__(self) -> None:
        self.running_interface_conf = None
        self.running_conf = None
        self.diff = None

    def vlan_merge_config_SVI(self, module_config, vlan_ids_list):
        commands = []
        key = f"interface vlan {vlan_ids_list[0]}"
        self.diff["interfaces"][key] = self.diff["interfaces"].get(key, [])
        Key_data_list = self.running_interface_conf.get(key, [])
        cmds, self.diff = config_ip_address(module_config, config_list=Key_data_list, diff=self.diff, key=key)
        if cmds:
            commands.extend(['config terminal', key])
            commands.extend(cmds)
            commands.extend(['end', 'save'])
        return commands

    def vlan_merge_config_anycast_gateway(self, module_config, vlan_ids_list):
        commands = []
        key = f"interface vlan {vlan_ids_list[0]}"
        self.diff["interfaces"][key] = self.diff["interfaces"].get(key, [])
        Key_data_list = self.running_interface_conf.get(key, [])
        cmds, self.diff = config_anycast_gateway(module_config, config_list=Key_data_list, diff=self.diff, key=key)
        if cmds:
            commands.extend(['config terminal', key])
            commands.extend(cmds)
            commands.extend(['end', 'save'])
        return commands

    def vlan_merge_config_ethernet(self, module_config, module_config_pch_ids, module_config_ports, vlan_ids_list):
        commands = []
        # for eth in module_config.get("interfaces", []):  Ethernet214
        for eth in module_config_ports:
            configured_pch_interfaces = []
            for pch in module_config_pch_ids:
                configured_pch_interfaces.extend(
                    get_portchannel_member_interfaces(self.running_interface_conf, pch))

            if eth not in configured_pch_interfaces:
                key = f"interface ethernet {eth}"
                self.diff["interfaces"][key] = self.diff["interfaces"].get(key, [])
                init_config_cmds = ['config terminal', key]
                commands.extend(init_config_cmds)
                config_list_pch = self.running_interface_conf.get(key, [])
                access_conf = get_substring_starstwith_matched_item_list("switchport access vlan", config_list_pch)
                trunk_conf = get_substring_starstwith_matched_item_list("switchport mode trunk", config_list_pch)
                if module_config.get('vlan_mode') == "trunk":
                    if access_conf:
                        commands.append(f"no {access_conf}")
                        self.diff["interfaces"][key].append(f"- {access_conf}")
                    commands.append(f"switchport mode trunk")
                    self.diff["interfaces"][key].append(f"+ switchport mode trunk")
                    for vl in vlan_ids_list:
                        cmd = f"switchport trunk allowed vlan add {vl}"
                        if cmd not in config_list_pch:
                            self.diff["interfaces"][key].append(f"+ {cmd}")
                            commands.append(f"switchport trunk allowed vlan add {vl}")
                else:
                    cmd = f"switchport access vlan {vlan_ids_list[0]}"
                    if trunk_conf:
                        trunk_lst = get_list_substring_starstwith_matched_item_list("switchport trunk allowed",
                                                                                    config_list_pch)
                        for t_l in trunk_lst:
                            commands.append(f"no {t_l}")
                            self.diff["interfaces"][key].append(f"- {t_l}")
                        commands.append(f"no switchport mode trunk")
                        self.diff["interfaces"][key].append(f"- switchport mode trunk")
                    elif access_conf and cmd != access_conf:
                        commands.append(f"no {access_conf}")
                        self.diff["interfaces"][key].append(f"- {access_conf}")
                    if cmd not in config_list_pch:
                        commands.append(f"switchport mode access")
                        commands.append(cmd)
                        self.diff["interfaces"][key].append(f"+ switchport mode access")
                        self.diff["interfaces"][key].append(f"+ {cmd}")
                commands.extend(["end", "save"])
        return commands

    def vlan_merge_config_pch(self, module_config, module_config_pch_ids, vlan_ids_list):
        commands = []
        # for pch in module_config.get("interfaces" []):  "pch10", "20", "portchannel30"
        for pch in module_config_pch_ids:
            configured_pch_interfaces = get_portchannel_member_interfaces(self.running_interface_conf, pch)
            for inf in configured_pch_interfaces:
                flag = True
                key_inf = f"interface ethernet {inf}"
                config_list_inf = self.running_interface_conf.get(key_inf, [])
                trunk_lst = get_list_substring_starstwith_matched_item_list("switchport trunk allowed",
                                                                            config_list_inf)
                access_conf = get_substring_starstwith_matched_item_list("switchport access vlan", config_list_inf)
                commands.append(f"config terminal")
                commands.append(key_inf)
                self.diff["interfaces"][key_inf] = []
                if trunk_lst:
                    flag = False
                    for t_l in trunk_lst:
                        commands.append(f"no {t_l}")
                        self.diff["interfaces"][key_inf].append(f"- {t_l}")
                    commands.append(f"no switchport mode trunk")
                    self.diff["interfaces"][key_inf].append(f"- switchport mode trunk")
                elif access_conf:
                    flag = False
                    commands.append(f"no {access_conf}")
                    self.diff["interfaces"][key_inf].append(f"- {access_conf}")
                if flag:
                    commands = commands[:-2]
                else:
                    commands.extend(["end", "save"])

            key = f"interface port-channel {pch}"
            self.diff["interfaces"][key] = self.diff["interfaces"].get(key, [])
            init_config_cmds = ['config terminal', key]
            commands.extend(init_config_cmds)
            config_list_pch = self.running_interface_conf.get(key, [])
            access_conf = get_substring_starstwith_matched_item_list("switchport access vlan", config_list_pch)
            trunk_conf = get_substring_starstwith_matched_item_list("switchport mode trunk", config_list_pch)
            if module_config.get('vlan_mode') == "trunk":
                if access_conf:
                    commands.append(f"no {access_conf}")
                    self.diff["interfaces"][key].append(f"- {access_conf}")
                commands.append(f"switchport mode trunk")
                self.diff["interfaces"][key].append(f"+ switchport mode trunk")
                for vl in vlan_ids_list:
                    cmd = f"switchport trunk allowed vlan add {vl}"
                    if cmd not in config_list_pch:
                        self.diff["interfaces"][key].append(f"+ {cmd}")
                        commands.append(f"switchport trunk allowed vlan add {vl}")
            else:
                cmd = f"switchport access vlan {vlan_ids_list[0]}"
                if trunk_conf:
                    trunk_lst = get_list_substring_starstwith_matched_item_list("switchport trunk allowed",
                                                                                config_list_pch)
                    for t_l in trunk_lst:
                        commands.append(f"no {t_l}")
                        self.diff["interfaces"][key].append(f"- {t_l}")
                    commands.append(f"no switchport mode trunk")
                    self.diff["interfaces"][key].append(f"- switchport mode trunk")
                elif access_conf and cmd != access_conf:
                    commands.append(f"no {access_conf}")
                    self.diff["interfaces"][key].append(f"- {access_conf}")
                if cmd not in config_list_pch:
                    commands.append(f"switchport mode access")
                    commands.append(cmd)
                    self.diff["interfaces"][key].append(f"+ switchport mode access")
                    self.diff["interfaces"][key].append(f"+ {cmd}")
            commands.extend(["end", "save"])
        return commands

    def vlans_merge_config(self, module):
        commands = []
        module_config_list = module.params['config']

        for module_config in module_config_list:
            vlan_ids_list = get_vlan_ids(module_config)
            # self.diff["vlan"][key] = []
            cmds, self.diff = config_vlans(module_config, config_list=self.running_conf, diff=self.diff)
            commands.extend(cmds)

            # SVI configuration
            # configure IP for the vlan_id or only for the first item of vlan_ids list
            if module_config['ip_address']:
                cmds = self.vlan_merge_config_SVI(module_config, vlan_ids_list)
                commands.extend(cmds)

            if module_config['anycast_gateway']:
                cmds = self.vlan_merge_config_anycast_gateway(module_config, vlan_ids_list)
                commands.extend(cmds)

            module_pch = [pid for pid in module_config.get("interfaces", []) if
                                     "ethernet" not in pid.lower()]
            module_config_pch_ids = []

            for s in module_pch:
                pch_id_str = "".join([c for c in str(s) if c.isdigit()])
                module_config_pch_ids.append(pch_id_str)
            module_config_ports = [prt for prt in module_config.get("interfaces", []) if "ethernet" in prt.lower()]

            # for pch in module_config.get("pch_id"):
            cmds = self.vlan_merge_config_pch(module_config, module_config_pch_ids, vlan_ids_list)
            commands.extend(cmds)

            # for eth in module_config.get("interfaces", []):
            cmds = self.vlan_merge_config_ethernet(module_config, module_config_pch_ids, module_config_ports,
                                                   vlan_ids_list)
            commands.extend(cmds)
        return commands

    def delete_vlans_interfaces_config(self, vlan_id, interfaces=[]):
        commands = []
        interfaces_data = self.running_interface_conf
        if interfaces:
            interfaces_data = {}
            module_pch_interface_key = []
            for intf in interfaces:
                if "ethernet" not in intf.lower():
                    pch_id_str = "".join([c for c in str(intf) if c.isdigit()])
                    module_pch_interface_key.append(f"interface port-channel {pch_id_str}")
                else:
                    module_pch_interface_key.append(f"interface ethernet {intf}")
            for key in module_pch_interface_key:
                if key in self.running_interface_conf:
                    interfaces_data[key] = self.running_interface_conf[key]
        for key, value in interfaces_data.items():
            trunk_vlan_cmd = f"switchport trunk allowed vlan add {vlan_id}"
            access_vlan_cmd = f"switchport access vlan {vlan_id}"
            trunk_lst = get_list_substring_starstwith_matched_item_list("switchport trunk allowed", value)
            trunk_vlan_id_list = get_list_substring_starstwith_matched_item_list(trunk_vlan_cmd, value)
            access_lst = get_substring_starstwith_matched_item_list(access_vlan_cmd, value)
            if trunk_vlan_id_list:
                commands.extend(["config", key])
                self.diff["interfaces"][key] = self.diff["interfaces"].get(key, [])
                cmd = f"no {trunk_vlan_cmd}"
                commands.append(cmd)
                self.diff["interfaces"][key].append(f"- {cmd}")
                if len(trunk_lst) == 1:
                    cmd = f"no switchport mode trunk"
                    commands.append(cmd)
                    self.diff["interfaces"][key].append(f"- {cmd}")
                commands.extend(["end", "save"])
            elif access_lst:
                commands.extend(["config", key])
                cmd = f"no {access_vlan_cmd}"
                commands.extend([cmd, "end", "save"])
                self.diff["interfaces"][key] = [f"- {cmd}"]
        return commands

    def cleanup_vlan_svi_config(self, vlan_id):
        # interface vlan 100
        commands = []
        self.diff["cleanup"] = "inside cleanup"
        key = f"interface vlan {vlan_id}"
        if key in self.running_interface_conf:
            self.diff["interfaces"][key] = self.diff["interfaces"].get(key, [])
            commands.append(f"config")
            if len(self.running_interface_conf.get(key)) >= 1:
                commands.append(key)
                for item in self.running_interface_conf.get(key):
                    commands.append(f"no {item}")
                    self.diff["interfaces"][key].append(f"- {item}")
                commands.append("exit")
            commands.append(f"no {key}")
            self.diff["interfaces"][key].append(f"- {key}")
            commands.extend(["end", "save"])
        return commands

    def delete_vlan_svi_config(self, vlan_id, ip_address):
        commands = []
        key = f"interface vlan {vlan_id}"
        if key in self.running_interface_conf:
            configs_value = self.running_interface_conf.get(key)
            self.diff["interfaces"][key] = self.diff["interfaces"].get(key, [])
            if len(configs_value) >= 1:
                ip_adds = get_list_substring_starstwith_matched_item_list(f"ip address {ip_address}", configs_value)
                if ip_adds:
                    commands.extend(["config", key])
                    commands.append(f"no {ip_adds[0]}")
                    self.diff["interfaces"][key].append(f"- {ip_adds[0]}")
                    commands.extend(["end", "save"])
        return commands

    def delete_vlan_anycast_gateway_config(self, vlan_id, ip_address):
        # interface vlan 100
        commands = []
        key = f"interface vlan {vlan_id}"
        if key in self.running_interface_conf:
            configs_value = self.running_interface_conf.get(key)
            self.diff["interfaces"][key] = self.diff["interfaces"].get(key, [])
            if len(configs_value) >= 1:
                ip_adds = get_list_substring_starstwith_matched_item_list(f"anycast-gateway {ip_address}",
                                                                          configs_value)
                if ip_adds:
                    commands.extend(["config", key])
                    commands.append(f"no {ip_adds[0]}")
                    self.diff["interfaces"][key].append(f"- {ip_adds[0]}")
                    commands.extend(["end", "save"])
        return commands

    def cleanup_vlans(self, vlan_id):
        commands = []
        cmds = self.delete_vlans_interfaces_config(vlan_id)
        commands.extend(cmds)
        cmds = self.cleanup_vlan_svi_config(
            vlan_id)  # it will delete "ip_address" and "anycast_gateway" both along with "interface vlan vlan_id"
        commands.extend(cmds)
        key = f"vlan {vlan_id}"
        if key in self.running_conf["vlan"]:
            self.diff["vlan"][key] = []
            commands.append(f"config")
            if len(self.running_conf["vlan"].get(key)) >= 1:
                commands.append(key)
                for item in self.running_conf["vlan"].get(key):
                    commands.append(f"no {item}")
                    self.diff["vlan"][key].append(f"- {item}")
                commands.append("exit")
            commands.append(f"no {key}")
            self.diff["vlan"][key].append(f"- {key}")
            commands.extend(["end", "save"])
        return commands

    def delete_vlan_config(self, module):
        commands = []
        module_config_list = module.params['config']
        delete_configs = ['vlan_ids', 'vlan_id', 'name', 'vrf_name', 'interfaces', 'ip_address', 'anycast_gateway']
        for module_config in module_config_list:
            vlan_ids_list = get_vlan_ids(module_config)
            filtered_module_config = {key: value for key, value in module_config.items() if
                                      value is not None and value not in ('', [])}
            delete_vlan_item = [item for item in list(filtered_module_config.keys()) if item in delete_configs]
            for v_id in vlan_ids_list:
                if len(delete_vlan_item) == 1 and delete_vlan_item[0] in ('vlan_ids', 'vlan_id'):
                    cmds = self.cleanup_vlans(vlan_id=v_id)
                    commands.extend(cmds)
                else:
                    if 'name' in delete_vlan_item:
                        pass
                    if 'vrf_name' in delete_vlan_item:
                        pass
                    if 'interfaces' in delete_vlan_item:
                        interfaces = module_config.get("interfaces", [])
                        cmds = self.delete_vlans_interfaces_config(vlan_id=v_id, interfaces=interfaces)
                        commands.extend(cmds)
                    if 'ip_address' in delete_vlan_item:
                        cmds = self.delete_vlan_svi_config(vlan_id=v_id, ip_address=module_config['ip_address'])
                        commands.extend(cmds)
                    if 'anycast_gateway' in delete_vlan_item:
                        cmds = self.delete_vlan_anycast_gateway_config(vlan_id=v_id,
                                                                       ip_address=module_config['anycast_gateway'])
                        commands.extend(cmds)
        return commands

    def get_config_commands(self, module, get_current_config=True):
        self.diff = {"interfaces": {}, "vlan": {}}
        # self.diff = {"vlan": {}}
        # module.params['config']

        # if get_current_config:
        self.running_conf = SonicConfig().get_running_configs(module)
        self.running_interface_conf = self.running_conf['interfaces']

        if module.params['state'] in ["delete"]:
            commands = self.delete_vlan_config(module)
        else:
            commands = self.vlans_merge_config(module)

        return commands, self.diff
