
from __future__ import absolute_import, division, print_function
from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.configs.sonic_config.sonic_config import SonicConfig


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
            if module['map_name']:
                commands.append(f"ip protocol bgp route-map {module['map_name']}")
            if module['action']:
                commands.append(f"route-map {module['map_name']} {module['action']} {module['sequence_num']} ")
                if module['set']['ip']:
                    commands.append(f"set src {module['set']['ip']}")
            commands.append('end')
            commands.append('save')
        return commands

    def get_config_commands(self, module, get_current_config=True):
        commands= list()
        self.diff = {}
        if get_current_config:
            self.running_bgp_conf = SonicConfig().get_running_configs(module)

        if module.params['state'] in ["delete"]:
            commands.extend(self.delete_config(module))
        else:
            commands.extend(self.config_bgpprotocol(module))      
        return  commands, self.diff 
