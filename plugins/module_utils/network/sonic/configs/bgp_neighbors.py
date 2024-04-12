from __future__ import absolute_import, division, print_function
from ansible_collections.aviznetworks.ansible.plugins.module_utils.network.sonic.configs.sonic_config.sonic_config import SonicConfig


class BGPNeighborsConfig(object):
    def __init__(self) -> None:
        pass

    def delete_config(self, module):
        commands = list()
        module_config = module.params['config']
        key_cmd = f"router bgp {module_config['bgp_asn']}"

    def config_neighbor(self, module):
        commands = list()
        module_config_list = module.params['config']
        for module_config in module_config_list:
            key_cmd = f"router bgp {module_config['bgp_asn']}"
            commands.append('config terminal')
            commands.append(key_cmd)
            current_cfg = self.running_bgp_conf.get(key_cmd, [])
            ipv4_config = module_config["neighbor"].get('ipv4')
            remote_as = ipv4_config.get("remote_as")  
            extended_nexthop = ipv4_config.get("extended_nexthop")
            for item in ipv4_config["ip"]:
                if remote_as:               
                    cmd = f"neighbor {item} remote-as {remote_as}"
                    if cmd not in current_cfg:
                        commands.append(cmd)    
                if extended_nexthop:
                    cmd = f"neighbor {item} capability extended-nexthop"
                    if cmd not in current_cfg:
                        commands.append(cmd)
            commands.append('end')
            commands.append('save')
        return commands


    def get_config_commands(self, module, get_current_config=True):
        commands= list()
        self.diff = {}
        if get_current_config:
            self.running_bgp_conf = SonicConfig().get_running_configs(module)["bgp"]
        if module.params['state'] in ["delete"]:
            commands.extend(self.delete_config(module))
        else:
            commands.extend(self.config_neighbor(module))      
        return commands, self.diff 