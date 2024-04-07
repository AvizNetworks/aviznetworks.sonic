from __future__ import absolute_import, division, print_function
from ansible_collections.aviznetworks.ansible.plugins.module_utils.network.sonic.configs.sonic_config.sonic_config import \
    SonicConfig
from ansible_collections.aviznetworks.ansible.plugins.module_utils.network.sonic.utils.utils import (
    get_substring_starstwith_matched_item_list,
    substring_starstwith_check)
from ansible_collections.aviznetworks.ansible.plugins.module_utils.network.sonic.utils.interfaces_util import config_ip_address
from ansible_collections.aviznetworks.ansible.plugins.module_utils.network.sonic.configs.svi import SVIConfig
from ansible_collections.aviznetworks.ansible.plugins.module_utils.network.sonic.argspecification.svi import SVIArgs

# from ansible_collections.aviznetworks.sonic_fmcli.plugins.module_utils.network.sonic.utils.interfaces_util

class MLAGConfig(object):

    def __init__(self) -> None:
        pass

    def delete_config(self, module):
        commands = []
        module_config_list = module.params['config']
        delete_configs = ['domain_id','peer_address', 'peer_link', 'src_address', 'member_port_channel','local_interface']
        for module_config in module_config_list:
            filtered_module_config = {key: value for key, value in module_config.items() if
                                      value is not None and value not in ('', [])}
            delete_mlag = [item for item in list(filtered_module_config.keys()) if item in delete_configs]
            key = f"mlag domain-id {module_config['domain_id']}"
            self.diff["mlag"][key] = []
            if key in self.running_pch_conf:
                commands.append(f"config terminal")
                if len(delete_mlag) == 1:
                    # mlag_conf = self.running_pch_conf[key]
                    # for item in mlag_conf:
                    #     commands.append(f"no {item}")
                    #     self.diff["mlag"][key].append(f"- {item}")
                    commands.append(f"no {key}")
                    self.diff["mlag"][key].append(f"- {key}")
                else:
                    config_list = self.running_pch_conf.get(key, [])
                    commands.append(key)
                    if module_config['peer_address']:
                        cmd = f"peer-address {module_config['peer_address']}"
                        if cmd in config_list:
                            commands.append(f"no {cmd}")
                            self.diff["mlag"][key].append(f"-{cmd}")
                    if module_config['peer_link']:
                        cmd = f"peer-link port-channel {module_config['peer_link']}"
                        if cmd in config_list:
                            commands.append(f"no {cmd}")
                            self.diff["mlag"][key].append(f"-{cmd}")
                    if module_config['src_address']:
                        cmd = f"src-address {module_config['src_address']}"
                        if cmd in config_list:
                            commands.append(f"no {cmd}")
                            self.diff["mlag"][key].append(f"-{cmd}")
                    if module_config['local_interface']:
                        cmd = f"local-interface vlan {module_config['local_interface']}"
                        if cmd in config_list:
                            commands.append(f"no {cmd}")
                            self.diff["mlag"][key].append(f"-{cmd}")
                    if module_config['member_port_channel']:
                        for  member in module_config['member_port_channel']:
                            cmd = f"member port-channel {member}"
                            if cmd in config_list:
                                commands.append(f"no {cmd}")
                                self.diff["mlag"][key].append(f"-{cmd}")
                    commands.append("exit")
                    commands.append(f"no {key}")
                commands.extend(['end', 'save'])
        return commands

    def create_mlag_domain(self, module):  
        commands = []
        module_config_list = module.params['config']
        
        for module_config in module_config_list:
            if module_config['domain_id']:
                key = f"mlag domain-id {module_config['domain_id']}"
                self.diff["mlag"][key] = []
                init_config_cmds = ['config terminal', key]
                commands.extend(init_config_cmds)
                config_list = self.running_pch_conf.get(key, [])
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

                cmd = f"peer-link port-channel {module_config['peer_link']}"
                if cmd in config_list:
                    pass
                elif substring_starstwith_check("peer-link", config_list):
                    cmd_dlt = get_substring_starstwith_matched_item_list("peer-link", config_list)
                    commands.append(f"no {cmd_dlt}")
                    commands.append(cmd)
                    self.diff["mlag"][key].append(f"- {cmd_dlt}")
                    self.diff["mlag"][key].append(f"+ {cmd}")
                else:
                    commands.append(cmd)
                    self.diff["mlag"][key].append(f"+ {cmd}")

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

                if len(module_config['member_port_channel']) > 1:
                    for member_pch in  module_config['member_port_channel']:
                        cmd = f"member port-channel {member_pch}"
                        if cmd in config_list:
                            pass
                        elif substring_starstwith_check("member port-channel", config_list):
                            cmd_dlt = get_substring_starstwith_matched_item_list("local-interface", config_list)
                            commands.append(f"no {cmd_dlt}")
                            commands.append(cmd)
                            self.diff["mlag"][key].append(f"- {cmd_dlt}")
                            self.diff["mlag"][key].append(f"+ {cmd}")
                        else:
                            commands.append(cmd)
                            self.diff["mlag"][key].append(f"+ {cmd}")

            commands.extend(["end", "save"])
        return commands

    def get_config_commands(self, module, get_current_config=True):
        commands = list()
        self.diff = {"mlag": {}}
        if get_current_config:
            self.running_pch_conf = SonicConfig().get_running_configs(module)["mlag"]
        if module.params['state'] in ["delete"]:
            commands.extend(self.delete_config(module))

        else: 
            commands.extend(self.create_mlag_domain(module))
        
            #commands, self.diff = commands.extend(self.create_mlag_domain(module))
        
        # if get_current_config:
        #     SonicConfig().get_running_configs(module)

        return commands, self.diff