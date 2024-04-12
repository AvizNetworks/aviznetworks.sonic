from __future__ import absolute_import, division, print_function
from ansible_collections.aviznetworks.ansible.plugins.module_utils.network.sonic.configs.sonic_config.sonic_config import SonicConfig


class BGPConfig(object):
    def __init__(self) -> None:
        pass
    def delete_config(self, module):
        commands = list()
        module_config = module.params['config']
        if module_config['protocol_bgp_route_map_name']:
            commands.append('config terminal')
            commands.append(f"ip protocol bgp route-map {module_config['protocol_bgp_route_map_name']}")
            commands.append('end')
            commands.append('save')
            
        key_cmd = f"router bgp {module_config['bgp_asn']}"
        if module_config["bgp"]:
            for bgp in module_config["bgp"]:
                commands.append('config terminal')
                commands.append(key_cmd)
                if bgp['router_id']:
                    cmd = f"no bgp router-id {bgp['router_id']}"
                    commands.append(cmd)
                if bgp['bestpath'] is True:
                    cmd = "no bgp bestpath as-path multipath-relax"
                    commands.append(cmd)                 
                if bgp['restart_time']:
                    cmd = f"no bgp graceful-restart restart-time {bgp['restart_time']}"
                    commands.append(cmd)
                if bgp['stalepath_time']:
                    cmd = f"no bgp graceful-restart stalepath-time {bgp['stalepath_time']}"
                    commands.append(cmd)
                commands.append('end')
                commands.append('save')
        return commands

    def config_bgp(self, module):
        commands = list()
        module_config = module.params['config']
        key_cmd = f"router bgp {module_config['bgp_asn']}"
        current_cfg = self.running_bgp_conf.get(key_cmd, [])
        if module_config["bgp"]:
            for bgp in module_config["bgp"]:
                commands.append('config terminal')
                commands.append(key_cmd)
                if bgp['router_id']:
                    cmd = f"bgp router-id {bgp['router_id']}"
                    if cmd not in current_cfg:
                        commands.append(cmd)
                if bgp['bestpath'] is True:
                    cmd = "bgp bestpath as-path multipath-relax"
                    if cmd not in current_cfg:
                        commands.append(cmd)
                if bgp['ebgp_requires_policy'] is False:
                    cmd = "no bgp ebgp-requires-policy"
                    if cmd not in current_cfg:
                        commands.append(cmd)  
                if bgp['restart_time']:
                    cmd = f"bgp graceful-restart restart-time {bgp['restart_time']}"
                    if cmd not in current_cfg:
                        commands.append(cmd)
                if bgp['stalepath_time']:
                    cmd = f"bgp graceful-restart stalepath-time {bgp['stalepath_time']}"
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
            commands.extend(self.config_bgp(module))      
        return commands, self.diff 