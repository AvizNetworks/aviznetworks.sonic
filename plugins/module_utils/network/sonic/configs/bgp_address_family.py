from __future__ import absolute_import, division, print_function
from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.configs.sonic_config.sonic_config import SonicConfig


class BGPAddressFamilyConfig(object):
    def __init__(self) -> None:
        pass

    def delete_config_address_family(self, module):
        commands = list()

    def config_address_family(self, module):
        commands = list()
        module_config_list = module.params['config']
        for module_config in module_config_list:
            key_cmd = f"router bgp {module_config['bgp_asn']}"
            commands.append('config terminal')
            commands.append(key_cmd)
            bgp_cfg = self.running_bgp_conf.get(key_cmd, [])
            address_family_ipv4_config = module_config["address_family"].get('ipv4')
            neighbor_config = address_family_ipv4_config.get("neighbor")
            allowas_in=neighbor_config.get("allowas_in")
            route_reflector_client = neighbor_config.get("route_reflector_client")
            next_hop_self = neighbor_config.get("next_hop_self")
            network_config = address_family_ipv4_config.get("network")
            redistribute_config = address_family_ipv4_config.get("redistribute")
            if neighbor_config["ips"] or network_config or redistribute_config:
                key_cmd = ('address-family ipv4 unicast')
                commands.append(key_cmd)
                current_cfg = bgp_cfg.get(key_cmd, [])
                for item in neighbor_config["ips"]:
                    if allowas_in:               
                        cmd = f"neighbor {item} allowas-in {allowas_in}"
                        if cmd not in current_cfg:
                            commands.append(cmd)
                    if route_reflector_client is True:
                        cmd = f"neighbor {item} route-reflector-client"
                        if cmd not in current_cfg:
                            commands.append(cmd)
                    if next_hop_self is True:
                        cmd = f"neighbor {item} next-hop-self force"
                        if cmd not in current_cfg:
                            commands.append(cmd) 
                for netw in network_config:
                    cmd = f"network {netw}"
                    if cmd not in current_cfg:
                        commands.append(cmd)
                for redis in redistribute_config:
                    cmd = f"redistribute {redis}"
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
            commands.extend(self.delete_config_address_family(module))
        else: 
            commands.extend(self.config_address_family(module))      
        return commands, self.diff