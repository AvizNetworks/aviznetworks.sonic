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
    get_vlan_ids
)


class VlanConfig(object):

    def __init__(self) -> None:
        self.running_interface_conf = None
        self.running_conf = None
        self.diff = None

    def vlans_merge_config(self, module):
        commands = []
        module_config_list = module.params['config']

        for module_config in module_config_list:
            vlan_ids_list = get_vlan_ids(module_config)
            svi_flag = True
            # self.diff["vlan"][key] = []
            vlan_cmds, self.diff = config_vlans(module_config, config_list=self.running_conf, diff=self.diff)
            commands.extend(vlan_cmds)

            # SVI configuration
            # configure IP for the vlan_id or only for the first item of vlan_ids list
            if svi_flag and module_config['ip_address']:
                svi_flag = False
                key = f"interface vlan {vlan_ids_list[0]}"
                self.diff["interfaces"][key] = []
                Key_data_list = self.running_interface_conf.get(key, [])
                cmds, self.diff = config_ip_address(module_config, config_list=Key_data_list, diff=self.diff, key=key)
                if cmds:
                    commands.extend(['config terminal', key])
                    commands.extend(cmds)
                    commands.extend(['end', 'save'])

            module_config_pch_ids = [pid for pid in module_config.get("interfaces", []) if
                                     "ethernet" not in pid.lower()]
            module_config_pch_ids = [s for s in module_config_pch_ids if any(char.isdigit() for char in s)]
            module_config_ports = [prt for prt in module_config.get("interfaces", []) if "ethernet" in prt.lower()]

            # for pch in module_config.get("pch_id"):
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
                self.diff["interfaces"][key] = []
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

            # for eth in module_config.get("interfaces", []):
            for eth in module_config_ports:
                configured_pch_interfaces = []
                for pch in module_config_pch_ids:
                    configured_pch_interfaces.extend(
                        get_portchannel_member_interfaces(self.running_interface_conf, pch))

                if eth not in configured_pch_interfaces:
                    key = f"interface ethernet {eth}"
                    self.diff["interfaces"][key] = []
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

        return commands, self.diff

    def delete_vlan_config(self, module):
        commands = []
        module_config_list = module.params['config']

        # delete_configs = ['vlan_id', 'pch_id', 'interfaces']
        for module_config in module_config_list:

            for interface in module_config['interfaces']:
                flag_intf = None
                inf_key = f"interface ethernet {interface}"
                self.diff["interfaces"][inf_key] = []
                init_config_cmds = ['config terminal', inf_key]
                commands.extend(init_config_cmds)
                cmd = f"channel-group {module_config['pch_id']} mode active"
                intf_config_list = self.running_interface_conf.get(inf_key, [])
                if inf_key in self.running_interface_conf and cmd in intf_config_list:
                    flag_intf = False
                    commands.append(f"no {cmd}")
                    self.diff['interfaces'][inf_key].append(f"- {cmd}")

                    if module_config['mtu']:
                        cmd = f"mtu {module_config['mtu']}"
                        if cmd in intf_config_list:
                            commands.append(f"no {cmd}")
                            self.diff['interfaces'][inf_key].append(f"- {cmd}")

                    if module_config['speed']:
                        cmd = f"speed {module_config['speed']}"
                        if cmd in intf_config_list:
                            commands.append(f"no {cmd}")
                            self.diff['interfaces'][inf_key].append(f"- {cmd}")

                if flag_intf or (flag_intf is None):
                    commands = commands[:-2]
                else:
                    commands.extend(['end', 'save'])

            # flag_pch = False
            key_pch = f"interface port-channel {module_config['pch_id']}"
            self.diff["interfaces"][key_pch] = []
            if key_pch in self.running_interface_conf:
                commands.append(f"config terminal")
                commands.append(f"no {key_pch}")
                commands.extend(['end', 'save'])
        return commands

    def get_config_commands(self, module, get_current_config=True):
        commands = list()
        self.diff = {"interfaces": {}, "vlan": {}}
        # self.diff = {"vlan": {}}
        # module.params['config']

        # if get_current_config:
        self.running_conf = SonicConfig().get_running_configs(module)
        self.running_interface_conf = self.running_conf['interfaces']

        if module.params['state'] in ["delete"]:
            commands.extend(self.delete_pch(module))

        else:
            commands, self.diff = self.vlans_merge_config(module)

        # if get_current_config:
        #     SonicConfig().get_running_configs(module)

        return commands, self.diff
