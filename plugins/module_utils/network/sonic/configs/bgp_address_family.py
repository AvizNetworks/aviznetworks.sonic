from __future__ import absolute_import, division, print_function
from ansible_collections.aviznetworks.sonic_fmcli.plugins.module_utils.network.sonic.configs.sonic_config.sonic_config import SonicConfig


class BGPAddressFamilyConfig(object):
    def __init__(self) -> None:
        pass

    def delete_config(self, module):
        commands = list()

    def config_neighbor(self, module):
        commands = list()
        module_config = module.params['config']
        key_cmd = f"router bgp {module_config['bgp_asn']}"
        current_cfg = self.running_bgp_conf.get(key_cmd,[])
        for item in module_config['address_family']["ipv4"]:
            commands.append('config terminal')
            commands.append(key_cmd)
            commands.append(f'address-family ipv4 unicast')
            for ip in item['neighbor_ip']:
                if item['allowas_in']:
                    cmd = f"neighbor {ip} allowas-in {item['allowas_in']}"
                    if cmd not in current_cfg:
                        commands.append(cmd)
                if item['route_reflector_client'] is True:
                    cmd = f"neighbor {ip} route-reflector-client"
                    if cmd not in current_cfg:
                        commands.append(cmd)
                if item['next_hop_self'] is True:
                    cmd = f"neighbor {ip} next-hop-self force"
                    if cmd not in current_cfg:
                        commands.append(cmd)
            if item['network']:
                for netw in item['network']:
                    cmd = f"network {netw}"
                    if cmd not in current_cfg:
                        commands.append(cmd)
            if item['redistribute']:
                for redis in item['redistribute']:
                    cmd = f"redistribute {redis}"
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