from __future__ import absolute_import, division, print_function
from ansible_collections.aviznetworks.sonic_fmcli.plugins.module_utils.network.sonic.configs.sonic_config.sonic_config import SonicConfig


class BGPNeighborsConfig(object):
    def __init__(self) -> None:
        pass

    def delete_config(self, module):
        commands = list()
        module_config = module.params['config']
        key_cmd = f"router bgp {module_config['bgp_asn']}"

    def config_neighbor(self, module):
        commands = list()
        module_config = module.params['config']
        key_cmd = f"router bgp {module_config['bgp_asn']}"
        current_cfg = self.running_bgp_conf.get(key_cmd,[])
        if module_config["neighbor"]:
            for neighbour in module_config["neighbor"]:
                commands.append('config terminal')
                commands.append(key_cmd)
                for ip in neighbour["neighbor_ip"] :
                    if neighbour['remote_as']:
                        cmd = f"neighbor {ip} remote-as {neighbour['remote_as']}"
                        if cmd not in current_cfg:
                            commands.append(cmd)
                    if neighbour['extended_nexthop']:
                        cmd = f"neighbor {ip} capability extended-nexthop"
                        if cmd not in current_cfg:
                            commands.append(cmd)
                commands.append('end')
                commands.append('save')
        return commands


    def get_config_commands(self, module, get_current_config=True):
        
        if get_current_config:
            self.running_bgp_conf = SonicConfig().get_running_configs(module)["bgp"]
        if module.params['state'] in ["delete"]:
            self.delete_config(module)
        else:
            commands = self.config_neighbor(module)      
        return  commands