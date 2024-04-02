from __future__ import absolute_import, division, print_function
from ansible_collections.aviznetworks.sonic_fmcli.plugins.module_utils.network.sonic.configs.sonic_config.sonic_config import SonicConfig


class BGPProtocolConfig(object):
    def __init__(self) -> None:
        pass

    def delete_config(self, module):
        commands = list()
        module_config = module.params['config']


    def config_bgpprotocol(self, module):
        commands = list()
        module_config = module.params['config']
        for module in module_config:
            commands.append('config terminal')
            if module['protocol_bgp_route_map_name']:
                commands.append(f"ip protocol bgp route-map {module['protocol_bgp_route_map_name']}")
            if module['permit_no'] and module['protocol_bgp_route_map_name']:
                commands.append(f"route-map {module['protocol_bgp_route_map_name']} permit {module['permit_no']} ")
                if module['src_ip']:
                    commands.append(f"set src {module['src_ip']}")
            commands.append('end')
            commands.append('save')
        return commands


    def get_config_commands(self, module, get_current_config=True):
        
        if get_current_config:
            self.running_bgp_conf = SonicConfig().get_running_configs(module)["bgp"]

        if module.params['state'] in ["delete"]:
            self.delete_config(module)
        else:
            commands = self.config_bgpprotocol(module)      
        return  commands