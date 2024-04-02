
from __future__ import absolute_import, division, print_function
from ansible_collections.aviznetworks.sonic_fmcli.plugins.module_utils.network.sonic.configs.sonic_config.sonic_config import SonicConfig


class BGPNeighborsConfig(object):
    def __init__(self) -> None:
        pass

    def config_neighbor(self, module):
        commands = list()
        module_config = module.params['config']
        key_cmd = f"router bgp {module_config['bgp_asn']}"
        current_cfg = self.running_bgp_conf[key_cmd]
        commands.append('config')
        commands.append('router bgp 2001')
        #         return commandsif module_config["neighbor"]:
        #     for neighbour in module_config["neighbor"]:
        #         commands.append('config terminal')
        #         commands.append(key_cmd)
        #         if neighbour["ip"] and neighbour['remote_as']:
        #           cmd = f"neighbor {neighbour['ip']} remote-as {neighbour['remote_as']}"
        #           if cmd not in current_cfg:
        #               commands.append(cmd)
        #         if neighbour["ip"] and neighbour['extended_nexthop']:
        #           cmd = f"neighbor {neighbour['ip']} capability extended-nexthop"
        #           if cmd not in current_cfg:
        #               commands.append(cmd)

        #         commands.append('end')
        #         commands.append('save')
        commands.append('end')
        commands.append('save')
        return commands


    def get_config_commands(self, module, get_current_config=True):
        
        if get_current_config:
            self.running_bgp_conf = SonicConfig().get_running_configs(module)["bgp"]
            
        commands = self.config_neighbor(module)

        # cmd2 = f"neighbor {module_config_list['neighbor'][0]['ip']} remote-as {module_config_list['neighbor'][0]['remote_as']}"
        # cmd2 = f"{module_config_list['neighbor'][0]['ip']}"
        # commands.extend(init_config_cmds)
        # commands.append(cmd2)
        # neibhbor_module_config_list = module.params['config']['neighbor']
        # commands.append(f"neighbor {neibhbor_module_config_list['ip']} ")
        # if module.params['state'] in ["delete"]:
        #     print("Hello")
        # else: 
        #     for module_config in module_config_list:
        #         self.configneighbor(commands, module_config['bgp_asn'] )
                # if not module_config['interface'] and module_config['vlan_id']:
                #     self.configvlan(commands, module_config['vlan_id'])
                # if module_config['vlan_mode'] and module_config['interface'] and module_config['vlan_id']:
                #     self.configaccesstrunk(commands, module_config['vlan_mode'], module_config['interface'], 
                #                            module_config['vlan_id'])       
        return  commands
