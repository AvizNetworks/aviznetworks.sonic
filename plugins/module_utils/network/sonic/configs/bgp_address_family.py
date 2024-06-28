from __future__ import absolute_import, division, print_function
from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.configs.sonic_config.sonic_config import \
    SonicConfig
from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.utils.utils import (
    get_substring_starstwith_matched_item_list)


class BGPAddressFamilyConfig(object):
    def __init__(self) -> None:
        self.running_bgp_conf = None
        self.diff = None

    def delete_config_l2vpn(self, module_config, cleanup=False):
        commands = []

        key_router = f"router bgp {module_config['bgp_asn']}"
        key_cmd = 'address-family l2vpn evpn'
        running_cfg_router = self.running_bgp_conf.get(key_router, {})

        if cleanup and key_cmd in running_cfg_router:
            module_config["address_family"] = {"l2vpn": {}}

        if module_config.get("address_family") and module_config["address_family"].get("l2vpn"):
            running_cfg_l2vpn = []
            if running_cfg_router:
                running_cfg_l2vpn = running_cfg_router.get(key_cmd, [])
            self.diff[key_router] = {"l2vpn": []}

            address_family_l2vpn = module_config["address_family"].get('l2vpn')
            advertise_all_vni = address_family_l2vpn.get("advertise_all_vni")
            neighbor_config = address_family_l2vpn.get("neighbor")
            flag = True

            if (not advertise_all_vni) and (not neighbor_config):
                running_cfg_l2vpn = running_cfg_l2vpn[::-1]
                commands.append('config terminal')
                commands.append(key_router)
                commands.append(key_cmd)
                flag = False
                for cfg in running_cfg_l2vpn:
                    commands.append(f"no {cfg}")
                    self.diff[key_router]["l2vpn"].append(f"- {cfg}")
                self.diff[key_router]["l2vpn"].append(f"- {key_cmd}")
                commands.extend(["exit", f"no {key_cmd}", "end", "save"])

            elif neighbor_config or advertise_all_vni:
                commands.append('config terminal')
                commands.append(key_router)
                commands.append(key_cmd)

                if advertise_all_vni:
                    cmd = get_substring_starstwith_matched_item_list("advertise-all-vni", running_cfg_l2vpn)
                    if cmd:
                        flag = False
                        commands.append("no advertise-all-vni")
                        self.diff[key_router]["l2vpn"].append("- advertise-all-vni")

                if neighbor_config:
                    for n_ip in neighbor_config.get("ips"):
                        if neighbor_config.get("activate"):
                            cmd = get_substring_starstwith_matched_item_list(f"neighbor {n_ip} activate",
                                                                             running_cfg_l2vpn)
                            if cmd:
                                flag = False
                                commands.append(f"no neighbor {n_ip} activate")
                                self.diff[key_router]["l2vpn"].append(f"- neighbor {n_ip} activate")

                        if neighbor_config.get("allowas_in"):
                            if neighbor_config.get("as_occurrence"):
                                cmd = get_substring_starstwith_matched_item_list(
                                    f"neighbor {n_ip} allowas-in {neighbor_config.get('as_occurrence')}",
                                    running_cfg_l2vpn)
                                if cmd:
                                    flag = False
                                    commands.append(f"no {cmd}")
                                    self.diff[key_router]["l2vpn"].append(f"- {cmd}")
            if flag:
                commands = commands[:-3]
            else:
                commands.extend(["end", "save"])
        return commands

    def delete_config_ipv6(self, module_config, cleanup=False):
        commands = []
        key_router = f"router bgp {module_config['bgp_asn']}"
        key_cmd = 'address-family ipv6 unicast'
        running_cfg_router = self.running_bgp_conf.get(key_router, {})
        if cleanup and key_cmd in running_cfg_router:
            module_config["address_family"] = {"ipv6": {}}

        if module_config.get("address_family") and module_config["address_family"].get("ipv6"):
            running_cfg_ipv6 = []
            if running_cfg_router:
                running_cfg_ipv6 = running_cfg_router.get(key_cmd, [])
            self.diff[key_router] = {"ipv6": []}

            address_family_ipv6 = module_config["address_family"].get('ipv6')
            advertise_all_vni = address_family_ipv6.get("advertise_all_vni")
            neighbor_config = address_family_ipv6.get("neighbor")
            redistribute_config = address_family_ipv6.get("redistribute")
            network = address_family_ipv6.get("network")
            max_path = address_family_ipv6.get("max_path")
            aggregate_address = address_family_ipv6.get("aggregate_address")
            flag = True

            if (not advertise_all_vni) and (not neighbor_config) and (not redistribute_config) and (not network) and (
                    not max_path) and (not aggregate_address):
                running_cfg_ipv6 = running_cfg_ipv6[::-1]
                commands.append('config terminal')
                commands.append(key_router)
                commands.append(key_cmd)
                flag = False
                for cfg in running_cfg_ipv6:
                    commands.append(f"no {cfg}")
                    self.diff[key_router]["ipv6"].append(f"- {cfg}")
                self.diff[key_router]["ipv6"].append(f"- {key_cmd}")
                commands.extend(["exit", f"no {key_cmd}", "end", "save"])

            elif neighbor_config or advertise_all_vni or redistribute_config or network or aggregate_address or max_path:
                commands.append('config terminal')
                commands.append(key_router)
                commands.append(key_cmd)
                for item in redistribute_config:
                    cmd = get_substring_starstwith_matched_item_list(f"redistribute {item}", running_cfg_ipv6)
                    if cmd:
                        flag = False
                        commands.append(f"no redistribute {item}")
                        self.diff[key_router]["ipv6"].append(f"- redistribute {item}")

                if flag:
                    commands = commands[:-3]
                else:
                    commands.extend(["end", "save"])

        return commands, self.diff

    def delete_config_ipv4(self, module_config, cleanup=False):
        commands = []
        return commands

    def delete_config_address_family(self, module):
        commands = list()
        module_config_list = module.params['config']
        for module_config in module_config_list:
            ipv4_cleanup = False
            ipv6_cleanup = False
            l2vpn_cleanup = False
            if not module_config.get("address_family"):
                ipv4_cleanup = True
                ipv6_cleanup = True
                l2vpn_cleanup = True

            cmds = self.delete_config_ipv4(module_config, cleanup=ipv6_cleanup)
            commands.extend(cmds)

            cmds = self.delete_config_ipv6(module_config, cleanup=ipv6_cleanup)
            commands.extend(cmds)

            cmds = self.delete_config_l2vpn(module_config, cleanup=l2vpn_cleanup)
            commands.extend(cmds)

    def config_ipv4(self, module_config):
        commands = []
        if module_config.get("address_family") and module_config["address_family"].get("ipv4"):
            key_cmd = f"router bgp {module_config['bgp_asn']}"
            commands.append('config terminal')
            commands.append(key_cmd)
            bgp_cfg = self.running_bgp_conf.get(key_cmd, [])
            address_family_ipv4_config = module_config["address_family"].get('ipv4')
            neighbor_config = address_family_ipv4_config.get("neighbor")
            allowas_in = neighbor_config.get("allowas_in")
            route_reflector_client = neighbor_config.get("route_reflector_client")
            next_hop_self = neighbor_config.get("next_hop_self")
            network_config = address_family_ipv4_config.get("network")
            redistribute_config = address_family_ipv4_config.get("redistribute")
            if neighbor_config["ips"] or network_config or redistribute_config:
                key_cmd = 'address-family ipv4 unicast'
                commands.append(key_cmd)
                current_cfg = bgp_cfg.get(key_cmd, [])
                for item in neighbor_config["ips"]:
                    if allowas_in:
                        cmd = f"neighbor {item} allowas-in {allowas_in}"
                        if cmd not in current_cfg:
                            commands.append(cmd)
                    if route_reflector_client is True:
                        cmd = f"neighbor {item} route-reflector-client"
                        if cmd not in current_cfg:
                            commands.append(cmd)
                    if next_hop_self is True:
                        cmd = f"neighbor {item} next-hop-self force"
                        if cmd not in current_cfg:
                            commands.append(cmd)
                for netw in network_config:
                    cmd = f"network {netw}"
                    if cmd not in current_cfg:
                        commands.append(cmd)
                for redis in redistribute_config:
                    cmd = f"redistribute {redis}"
                    if cmd not in current_cfg:
                        commands.append(cmd)
            commands.append('end')
            commands.append('save')
        return commands

    def config_ipv6(self, module_config):
        commands = []
        flag = True
        if module_config.get("address_family") and module_config["address_family"].get("ipv6"):
            key_router = f"router bgp {module_config['bgp_asn']}"
            key_cmd = 'address-family ipv6 unicast'
            running_cfg_router = self.running_bgp_conf.get(key_router, {})
            running_cfg_ipv6 = []
            if running_cfg_router:
                running_cfg_ipv6 = running_cfg_router.get(key_cmd, [])
            self.diff[key_router] = {"ipv6": []}

            address_family_ipv6 = module_config["address_family"].get('ipv6')
            advertise_all_vni = address_family_ipv6.get("advertise_all_vni")
            neighbor_config = address_family_ipv6.get("neighbor")
            redistribute_config = address_family_ipv6.get("redistribute")
            network = address_family_ipv6.get("network")
            max_path = address_family_ipv6.get("max_path")
            aggregate_address = address_family_ipv6.get("aggregate_address")

            if neighbor_config or advertise_all_vni or redistribute_config or network or aggregate_address or max_path:
                commands.append('config terminal')
                commands.append(key_router)
                commands.append(key_cmd)
                for item in redistribute_config:
                    if get_substring_starstwith_matched_item_list(f"redistribute {item}", running_cfg_ipv6) == "":
                        flag = False
                        commands.append(f"redistribute {item}")
                        self.diff[key_router]["ipv6"].append(f"+ redistribute {item}")

            if flag:
                commands = commands[:-3]
            else:
                commands.extend(["end", "save"])
        return commands

    def config_l2vpn(self, module_config):
        commands = []
        flag = True
        if module_config.get("address_family") and module_config["address_family"].get("l2vpn"):
            key_router = f"router bgp {module_config['bgp_asn']}"
            key_cmd = 'address-family l2vpn evpn'
            running_cfg_router = self.running_bgp_conf.get(key_router, {})
            running_cfg_l2vpn = []
            if running_cfg_router:
                running_cfg_l2vpn = running_cfg_router.get(key_cmd, [])
            self.diff[key_router] = {"l2vpn": []}

            address_family_l2vpn = module_config["address_family"].get('l2vpn')
            advertise_all_vni = address_family_l2vpn.get("advertise_all_vni")
            neighbor_config = address_family_l2vpn.get("neighbor")

            if neighbor_config or advertise_all_vni:
                commands.append('config terminal')
                commands.append(key_router)
                commands.append(key_cmd)

                if neighbor_config:
                    for n_ip in neighbor_config.get("ips"):
                        """
                        neighbor 40.0.0.8 activate
                        neighbor 40.0.0.0 allowas-in 1
                        """
                        if neighbor_config.get("activate"):
                            if get_substring_starstwith_matched_item_list(f"neighbor {n_ip} activate",
                                                                          running_cfg_l2vpn) == "":
                                flag = False
                                commands.append(f"neighbor {n_ip} activate")
                                self.diff[key_router]["l2vpn"].append(f"+ neighbor {n_ip} activate")
                        elif neighbor_config.get("activate") is False:
                            cmd = get_substring_starstwith_matched_item_list(f"neighbor {n_ip} activate",
                                                                             running_cfg_l2vpn)
                            if cmd:
                                flag = False
                                commands.append(f"no {cmd}")
                                self.diff[key_router]["l2vpn"].append(f"- {cmd}")

                        if neighbor_config.get("allowas_in"):
                            if neighbor_config["allowas_in"].get("as_occurrence") and neighbor_config["allowas_in"].get(
                                    "as_occurrence") != "None":
                                as_ocu_cmd = (f"neighbor {n_ip} allowas-in "
                                              f"{neighbor_config['allowas_in'].get('as_occurrence')}")
                                existing_allowes_on = get_substring_starstwith_matched_item_list(
                                    f"neighbor {n_ip} allowas-in", running_cfg_l2vpn)
                                if existing_allowes_on == "":
                                    flag = False
                                    commands.append(as_ocu_cmd)
                                    self.diff[key_router]["l2vpn"].append(f"+ {as_ocu_cmd}")
                                elif existing_allowes_on != as_ocu_cmd:
                                    flag = False
                                    # commands.append(f"no {existing_allowes_on}")
                                    commands.append(as_ocu_cmd)
                                    self.diff[key_router]["l2vpn"].append(f"- {existing_allowes_on}")
                                    self.diff[key_router]["l2vpn"].append(f"+ {as_ocu_cmd}")

                if advertise_all_vni:
                    if get_substring_starstwith_matched_item_list("advertise-all-vni", running_cfg_l2vpn) == "":
                        flag = False
                        commands.append("advertise-all-vni")
                        self.diff[key_router]["l2vpn"].append("+ advertise-all-vni")
                elif advertise_all_vni is False:
                    if get_substring_starstwith_matched_item_list("advertise-all-vni", running_cfg_l2vpn):
                        flag = False
                        commands.append("no advertise-all-vni")
                        self.diff[key_router]["l2vpn"].append("- advertise-all-vni")

        if flag:
            commands = commands[:-3]
        else:
            commands.extend(["end", "save"])
        return commands

    def config_address_family(self, module):
        commands = list()
        module_config_list = module.params['config']
        for module_config in module_config_list:
            cmds = self.config_ipv4(module_config)
            commands.extend(cmds)

            cmds = self.config_ipv6(module_config)
            commands.extend(cmds)

            cmds = self.config_l2vpn(module_config)
            commands.extend(cmds)

        return commands

    def get_config_commands(self, module, get_current_config=True):
        commands = list()
        self.diff = {}

        if get_current_config:
            self.running_bgp_conf = SonicConfig().get_running_configs(module)["bgp"]

        if module.params['state'] in ["delete"]:
            commands.extend(self.delete_config_address_family(module))
        else:
            commands.extend(self.config_address_family(module))
        return commands, self.diff
