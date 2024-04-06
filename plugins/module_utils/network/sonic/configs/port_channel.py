from __future__ import absolute_import, division, print_function
from ansible_collections.aviznetworks.ansible.plugins.module_utils.network.sonic.configs.sonic_config.sonic_config import SonicConfig
from ansible_collections.aviznetworks.ansible.plugins.module_utils.network.sonic.utils.utils import (
    get_substring_starstwith_matched_item_list,
    substring_starstwith_check)
from ansible_collections.aviznetworks.ansible.plugins.module_utils.network.sonic.utils.interfaces_util import (
    config_mtu,
    config_description,
    config_ip_address,
    config_speed,
    config_channel_group)


class PortchannelConfig(object):
    
    def __init__(self) -> None:
        pass

    
    def pch_merge_config(self, module):
        commands = []
        module_config_list = module.params['config'] 
        for module_config in module_config_list:
            flag_pch = None
            pch = module_config['pch_id']
            key = f"interface port-channel {pch}"
            self.diff["interfaces"][key] = []
            init_config_cmds = ['config terminal', key]
            commands.extend(init_config_cmds)
            if key not in self.running_pch_conf:
                flag_pch = False
            config_list = self.running_pch_conf.get(key, [])
            if module_config['mtu']:
                cmds, self.diff = config_mtu(module_config, config_list, diff=self.diff, key=key)
                commands.extend(cmds)
                flag_pch = True if (len(cmds) == 0) and (flag_pch is None) else False  
            if module_config['ip_address']:
                cmds, self.diff = config_ip_address(module_config, config_list, diff=self.diff, key=key)
                commands.extend(cmds)
                flag_pch = True if (len(cmds) == 0) and ((flag_pch is True) or (flag_pch is None)) else False
            if module_config['description']:
                cmds, self.diff = config_description(module_config, config_list, diff=self.diff, key=key)
                commands.extend(cmds)
                flag_pch = True if (len(cmds) == 0) and ((flag_pch is True) or (flag_pch is None)) else False
                
            if flag_pch or (flag_pch is None):
                commands = commands[:-2]
            else:
                commands.extend(['end', 'save'])

            for interface in module_config['interfaces']:
                flag_intf = None
                inf_key = f"interface ethernet {interface}"
                self.diff["interfaces"][inf_key] = []
                init_config_cmds = ['config terminal', inf_key]
                commands.extend(init_config_cmds)
                if inf_key not in self.running_pch_conf:
                    flag_intf = False
                intf_config_list = self.running_pch_conf.get(inf_key, [])
                if module_config['mtu']:
                    cmds, self.diff = config_mtu(module_config, intf_config_list, diff=self.diff, key=inf_key)
                    commands.extend(cmds)
                    flag_intf = True if (len(cmds) == 0) and ((flag_intf is True) or (flag_intf is None)) else False
                if module_config['speed']:
                    cmds, self.diff = config_speed(module_config, intf_config_list, diff=self.diff, key=inf_key)
                    commands.extend(cmds)
                    flag_intf = True if (len(cmds) == 0) and ((flag_intf is True) or (flag_intf is None)) else False

                cmds, self.diff = config_channel_group(module_config, intf_config_list, diff=self.diff, key=inf_key)
                commands.extend(cmds)
                flag_intf = True if (len(cmds) == 0) and ((flag_pch is True) or (flag_pch is None)) else False

                if flag_intf or (flag_intf is None):
                    commands = commands[:-2]
                else:
                    commands.extend(['end', 'save'])
        return commands


    def delete_pch(self, module):
        commands = []
        module_config_list = module.params['config']

        #delete_configs = ['interfaces', 'pch_id', 'description', 'mtu', 'mode']
        for module_config in module_config_list:
            
            for interface in module_config['interfaces']:
                flag_intf = None
                inf_key = f"interface ethernet {interface}"
                self.diff["interfaces"][inf_key] = []
                init_config_cmds = ['config terminal', inf_key]
                commands.extend(init_config_cmds)
                cmd = f"channel-group {module_config['pch_id']} mode active"
                intf_config_list = self.running_pch_conf.get(inf_key, []) 
                if inf_key in self.running_pch_conf and cmd in intf_config_list:
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
            if key_pch in self.running_pch_conf:
                commands.append(f"config terminal")
                commands.append(f"no {key_pch}")
                commands.extend(['end', 'save'])
        return commands
    
            
    def get_config_commands(self, module, get_current_config=True):
        commands = list()
        self.diff = {"interfaces": {}}
        module.params['config']

        if get_current_config:
            self.running_pch_conf = SonicConfig().get_running_configs(module)['interfaces']
        
            
        if module.params['state'] in ["delete"]:
            commands.extend(self.delete_pch(module))

        else:
            commands.extend(self.pch_merge_config(module))
        
        # if get_current_config:
        #     SonicConfig().get_running_configs(module)

        return commands, self.diff
        
