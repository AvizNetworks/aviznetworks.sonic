from __future__ import absolute_import, division, print_function
from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.configs.sonic_config.sonic_config import \
    SonicConfig
from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.utils.utils import (
    get_substring_starstwith_matched_item_list,
    substring_starstwith_check)
from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.utils.interfaces_util import \
    config_ip_address
from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.configs.svi import SVIConfig
from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.argspecification.svi import SVIArgs


# from ansible_collections.aviznetworks.sonic_fmcli.plugins.module_utils.network.sonic.utils.interfaces_util

class MLAGConfig(object):

    def __init__(self) -> None:
        self.running_interfaces_conf = None
        self.running_mlag_conf = None
        self.running_conf = None
        self.diff = None

    def delete_config(self, module):
        commands = []
        module_config_list = module.params['config']
        delete_configs = ['domain_id', 'peer_address', 'peer_link', 'src_address', 'member_portchannels',
                          'local_interface']
        for module_config in module_config_list:
            filtered_module_config = {key: value for key, value in module_config.items() if
                                      value is not None and value not in ('', [])}
            delete_mlag = [item for item in list(filtered_module_config.keys()) if item in delete_configs]
            key = f"mlag domain-id {module_config['domain_id']}"
            self.diff["mlag"][key] = self.diff["mlag"].get(key, [])
            if key in self.running_mlag_conf:
                commands.append(f"config terminal")
                if len(delete_mlag) == 1:
                    mlag_conf = self.running_mlag_conf[key]
                    if mlag_conf:
                        commands.append(key)
                        for item in mlag_conf:
                            commands.append(f"no {item}")
                            self.diff["mlag"][key].append(f"- {item}")
                        commands.append("exit")
                    commands.append(f"no {key}")
                    self.diff["mlag"][key].append(f"- {key}")
                else:
                    config_list = self.running_mlag_conf.get(key, [])
                    commands.append(key)
                    if module_config['peer_address']:
                        cmd = f"peer-address {module_config['peer_address']}"
                        if cmd in config_list:
                            commands.append(f"no {cmd}")
                            self.diff["mlag"][key].append(f"- {cmd}")
                    if module_config['peer_link']:
                        cmd = f"peer-link port-channel {module_config['peer_link']}"
                        if cmd in config_list:
                            commands.append(f"no {cmd}")
                            self.diff["mlag"][key].append(f"- {cmd}")
                        cmd = f"peer-link interface {module_config['peer_link']}"
                        if cmd in config_list:
                            commands.append(f"no {cmd}")
                            self.diff["mlag"][key].append(f"- {cmd}")
                    if module_config['src_address']:
                        cmd = f"src-address {module_config['src_address']}"
                        if cmd in config_list:
                            commands.append(f"no {cmd}")
                            self.diff["mlag"][key].append(f"- {cmd}")
                    if module_config['local_interface']:
                        cmd = f"local-interface vlan {module_config['local_interface']}"
                        if cmd in config_list:
                            commands.append(f"no {cmd}")
                            self.diff["mlag"][key].append(f"- {cmd}")
                    for member in module_config['member_portchannels']:
                        pch_id_str = "".join([c for c in str(member) if c.isdigit()])
                        cmd = f"member port-channel {pch_id_str}"
                        if cmd in config_list:
                            commands.append(f"no {cmd}")
                            self.diff["mlag"][key].append(f"- {cmd}")
                    commands.append("exit")
                    # commands.append(f"no {key}")
                commands.extend(['end', 'save'])

        return commands

    def config_peer_address(self, module_config, config_list, key):
        commands = []
        cmd = f"peer-address {module_config['peer_address']}"
        if cmd in config_list:
            pass
        elif substring_starstwith_check("peer-address", config_list):
            cmd_dlt = get_substring_starstwith_matched_item_list("peer-address", config_list)
            commands.append(f"no {cmd_dlt}")
            commands.append(cmd)
            self.diff["mlag"][key].append(f"- {cmd_dlt}")
            self.diff["mlag"][key].append(f"+ {cmd}")
        else:
            commands.append(cmd)
            self.diff["mlag"][key].append(f"+ {cmd}")

        return commands

    def config_peer_link_portchannel(self, module_config, config_list, key):
        commands = []
        peer_link = module_config['peer_link']
        if peer_link:
            if "ethernet" not in peer_link.lower():
                # commands.append(f"config terminal")
                pch_id = "".join([c for c in str(peer_link) if c.isdigit()])
                # pch_key = f"interface port-channel {pch_id}"
                # if pch_key not in self.running_interfaces_conf:
                #     commands.extend([pch_key, "exit"])

                cmd = f"peer-link port-channel {pch_id}"
                if cmd in config_list:
                    pass
                elif substring_starstwith_check("peer-link port-channel", config_list):
                    cmd_dlt = get_substring_starstwith_matched_item_list("peer-link port-channel", config_list)
                    commands.append(f"no {cmd_dlt}")
                    commands.append(cmd)
                    self.diff["mlag"][key].append(f"- {cmd_dlt}")
                    self.diff["mlag"][key].append(f"+ {cmd}")
                else:
                    commands.append(cmd)
                    self.diff["mlag"][key].append(f"+ {cmd}")
                return commands

    def config_peer_link_interface(self, module_config, config_list, key):
        commands = []
        peer_link = module_config['peer_link']
        if peer_link:
            if "ethernet" in peer_link.lower():
                cmd = f"peer-link interface {module_config['peer_link']}"
                if cmd in config_list:
                    pass
                elif substring_starstwith_check("peer-link interface", config_list):
                    cmd_dlt = get_substring_starstwith_matched_item_list("peer-link interface", config_list)
                    commands.append(f"no {cmd_dlt}")
                    commands.append(cmd)
                    self.diff["mlag"][key].append(f"- {cmd_dlt}")
                    self.diff["mlag"][key].append(f"+ {cmd}")
                else:
                    commands.append(cmd)
                    self.diff["mlag"][key].append(f"+ {cmd}")

        return commands

    def config_src_address(self, module_config, config_list, key):
        commands = []
        cmd = f"src-address {module_config['src_address']}"
        if cmd in config_list:
            pass
        elif substring_starstwith_check("src-address", config_list):
            cmd_dlt = get_substring_starstwith_matched_item_list("src-address", config_list)
            commands.append(f"no {cmd_dlt}")
            commands.append(cmd)
            self.diff["mlag"][key].append(f"- {cmd_dlt}")
            self.diff["mlag"][key].append(f"+ {cmd}")
        else:
            commands.append(cmd)
            self.diff["mlag"][key].append(f"+ {cmd}")

        return commands

    def config_local_interface_vlan(self, module_config, config_list, key):
        commands = []
        cmd = f"local-interface vlan {module_config['local_interface']}"
        if cmd in config_list:
            pass
        elif substring_starstwith_check("local-interface", config_list):
            cmd_dlt = get_substring_starstwith_matched_item_list("local-interface", config_list)
            commands.append(f"no {cmd_dlt}")
            commands.append(cmd)
            self.diff["mlag"][key].append(f"- {cmd_dlt}")
            self.diff["mlag"][key].append(f"+ {cmd}")
        else:
            commands.append(cmd)
            self.diff["mlag"][key].append(f"+ {cmd}")

        return commands

    def config_member_portchannel(self, module_config, config_list, key):
        commands = []
        if len(module_config['member_portchannels']) > 1:
            for member in module_config['member_portchannels']:
                pch_id_str = "".join([c for c in str(member) if c.isdigit()])
                cmd = f"member port-channel {pch_id_str}"
                if cmd not in config_list:
                    commands.append(cmd)
                    self.diff["mlag"][key].append(f"+ {cmd}")

        return commands

    def create_mlag_domain(self, module):
        commands = []
        module_config_list = module.params['config']

        for module_config in module_config_list:
            if module_config['domain_id']:
                key = f"mlag domain-id {module_config['domain_id']}"
                self.diff["mlag"][key] = self.diff["mlag"].get(key, [])
                init_config_cmds = ['config terminal', key]
                commands.extend(init_config_cmds)
                config_list = self.running_mlag_conf.get(key, [])

                peer_link_conf = self.config_peer_address(module_config, config_list, key)
                commands.extend(peer_link_conf)

                peer_link_pch_conf = self.config_peer_link_portchannel(module_config, config_list, key)
                commands.extend(peer_link_pch_conf)

                peer_link_interface_conf = self.config_peer_link_interface(module_config, config_list, key)
                commands.extend(peer_link_interface_conf)

                src_add_conf = self.config_src_address(module_config, config_list, key)
                commands.extend(src_add_conf)

                local_interface_conf = self.config_local_interface_vlan(module_config, config_list, key)
                commands.extend(local_interface_conf)

                member_portchannel_conf = self.config_member_portchannel(module_config, config_list, key)
                commands.extend(member_portchannel_conf)

            commands.extend(["end", "save"])
        return commands

    def get_config_commands(self, module, get_current_config=True):
        commands = list()
        self.diff = {"mlag": {}}
        if get_current_config:
            self.running_conf = SonicConfig().get_running_configs(module)
            self.running_mlag_conf = self.running_conf["mlag"]
            self.running_interfaces_conf = self.running_conf["interfaces"]
        if module.params['state'] in ["delete"]:
            commands.extend(self.delete_config(module))

        else:
            commands.extend(self.create_mlag_domain(module))

        return commands, self.diff