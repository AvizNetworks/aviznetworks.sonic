from __future__ import absolute_import, division, print_function
from ansible_collections.aviznetworks.ansible.plugins.module_utils.network.sonic.configs.sonic_config.sonic_config import SonicConfig


class VlanConfig(object):
    def __init__(self) -> None:
        pass

    def configvlan(self, commands, vlanid):
        for id in vlanid:
            commands.append(f"vlan {id}")
            commands.append(f"exit")
        return commands
    
    def configipaddress(self, commands, vlanid, ipaddress):
        commands.append(f"interface vlan {vlanid[0]}")
        commands.append(f"ip address {ipaddress}")
        commands.append(f"exit")
        return commands
    
    def unconfigipaddress(self, commands, vlanid, ipaddress):
        commands.append(f"no interface vlan {vlanid[0]}")
        return commands
    
    def unconfigvlan(self, commands, vlanid):
        for id in vlanid:
            commands.append(f"no vlan {id}")
        return commands


    def configaccesstrunk(self, commands, vlanmode, interface, vlanid):
        if vlanmode:
            for intf in interface:
                commands.append(f"interface ethernet {intf}")
                commands.append(f"switchport mode {vlanmode}")
                for id in vlanid:
                    if vlanmode.lower() == "access":
                        commands.append(f"switchport access vlan {id}")
                    else:
                        commands.append(f"switchport trunk allowed vlan add {id}")
                commands.append(f"exit") 
            return commands 

    def unconfigaccesstrunk(self, commands, interface, vlanid, vlanmode, switchport):
        for intf in interface:
            commands.append(f"interface ethernet {intf}")   
            if vlanmode.lower() == "access":
                commands.append(f"no switchport access vlan {vlanid[0]}")
            else:
                for portid in vlanid:  
                    commands.append(f"no switchport trunk allowed vlan add {portid}")
                if switchport:
                    commands.append(f"no switchport mode {vlanmode}")
            commands.append(f"exit")
        return commands

    def get_config_commands(self, module, get_current_config=True):
        
        # if get_current_config:
        #     running_config_json = SonicConfig().get_running_configs(module)
            

        commands = list()
        module_config_list = module.params['config']
        init_config_cmds = ['config terminal']
        commands.extend(init_config_cmds)

        if module.params['state'] in ["delete"]:
            for module_config in module_config_list:
                if not module_config['interface'] and module_config['vlan_id']:
                    self.unconfigvlan(commands, module_config['vlan_id'])
                if module_config['vlan_mode'] and module_config['interface'] and module_config['vlan_id']:
                    self.unconfigaccesstrunk(commands, module_config['interface'], module_config['vlan_id'],
                                             module_config['vlan_mode'], module_config['enableswitchport'])
                if module_config['ipaddress'] and module_config['vlan_id']:
                    self.unconfigipaddress(commands, module_config['vlan_id'], module_config['ipaddress'])   
        else: 
            for module_config in module_config_list:
                if not module_config['interface'] and module_config['vlan_id']:
                    self.configvlan(commands, module_config['vlan_id'])
                if module_config['vlan_mode'] and module_config['interface'] and module_config['vlan_id']:
                    self.configaccesstrunk(commands, module_config['vlan_mode'], module_config['interface'], 
                                           module_config['vlan_id']) 
                if module_config['ipaddress'] and module_config['vlan_id']:
                    self.configipaddress(commands, module_config['vlan_id'], module_config['ipaddress'])   
        return  commands