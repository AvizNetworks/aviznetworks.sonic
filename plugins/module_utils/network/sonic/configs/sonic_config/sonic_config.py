from __future__ import absolute_import, division, print_function

import json
import re

from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.sonic import run_commands


class SonicConfig(object):
    
    def __init__(self) -> None:
        pass
    
    def fmcli_config_to_json(self, fmcli_conf):
        fmcli_conf_json = {"metadata": {}, "vlan": {}, "interfaces": {}, "mlag": {},"route_map": {}, "vxlan": {}, "bgp": {}, "sag": {}}

        with open(fmcli_conf, "r") as fmcli:
            fmcli_conf_lines = fmcli.readlines()

        for count, line in enumerate(fmcli_conf_lines):
            line = line.rstrip() if "!" in line else line.strip()
            if line == "!":
                vlan_config = False
                interface_config = False
                mlag_config = False
                route_map_config = False
                vxlan_config = False
                router_bgp_config = False
                router_bgp_address_family_config = False
                sag_config = False
                key = ""
                inner_key = ""
            else:
                ip_regx = "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
                hostname_regx = "^hostname\s\S+$"
                router_id_ip_regx = f"^router-id\s{ip_regx}$"
                ntp_add_ip_regx = f"^ntp\sadd\s{ip_regx}$"
                clock_timezone_regx = f"^clock\stimezone\s\S+$"
                syslog_add_ip_regx = f"^syslog\sadd\s{ip_regx}$"
                snmp_server__ip_regx = f"snmp-server[\s\S]+{ip_regx}[\s\S]+$"
                ip_protocol_bgp_regx = f"^ip\sprotocol\sbgp\sroute\-map\s\S+$"

                if re.match(
                        f"{hostname_regx}|{router_id_ip_regx}|{ntp_add_ip_regx}|{clock_timezone_regx}|{syslog_add_ip_regx}|{snmp_server__ip_regx}|{ip_protocol_bgp_regx}",
                        line):
                    fmcli_conf_json[line] = ""
                # vlan json data
                elif route_map_config or re.match("^route\-map\s\w+\spermit\s\d+$", line):
                    route_map_config = True
                    if not key:
                        key = line
                        if key not in fmcli_conf_json["route_map"]:
                            fmcli_conf_json["route_map"][key] = []
                    else:
                        fmcli_conf_json["route_map"][key].append(line)

                elif vlan_config or re.match("^vlan\s\d+$", line):
                    vlan_config = True
                    if not key:
                        key = line
                        if key not in fmcli_conf_json["vlan"]:
                            fmcli_conf_json["vlan"][key] = []
                    else:
                        fmcli_conf_json["vlan"][key].append(line)

                elif vxlan_config or re.match("^vxlan\s\S+$", line):
                    vxlan_config = True
                    if not key:
                        key = line
                        if key not in fmcli_conf_json["vxlan"]:
                            fmcli_conf_json["vxlan"][key] = []
                    else:
                        fmcli_conf_json["vxlan"][key].append(line)

                # interface ethernet | vlan | loopback | port-channel json data
                elif interface_config or re.match("^interface\s(vlan|loopback|port-channel|ethernet)\s\S+$", line):
                    interface_config = True
                    if not key:
                        key = line
                        if key not in fmcli_conf_json["interfaces"]:
                            fmcli_conf_json["interfaces"][key] = []
                    else:
                        fmcli_conf_json["interfaces"][key].append(line)

                elif mlag_config or re.match("^mlag\sdomain\-id\s\d$", line):
                    mlag_config = True
                    if not key:
                        key = line
                        if key not in fmcli_conf_json["mlag"]:
                            fmcli_conf_json["mlag"][key] = []
                    else:
                        fmcli_conf_json["mlag"][key].append(line)

                elif router_bgp_config or re.match("^router\sbgp\s\d+$", line):
                    router_bgp_config = True
                    if not key:
                        key = line
                        if key not in fmcli_conf_json["bgp"]:
                            fmcli_conf_json["bgp"][key] = {}
                    elif line == " !":
                        router_bgp_address_family_config = False
                        inner_key = ""

                    elif router_bgp_address_family_config or re.match("^address-family\s\S+\s[unicast|evpn]+$", line):
                        router_bgp_address_family_config = True
                        if not inner_key:
                            inner_key = line
                            if inner_key not in fmcli_conf_json["bgp"][key]:
                                fmcli_conf_json["bgp"][key][inner_key] = []
                        else:
                            fmcli_conf_json["bgp"][key][inner_key].append(line)
                    else:
                        fmcli_conf_json["bgp"][key][line] = {}

                elif sag_config or re.match("^sag$", line):
                    sag_config = True
                    if not key:
                        key = line
                        if key not in fmcli_conf_json["sag"]:
                            fmcli_conf_json["sag"][key] = []
                    else:
                        fmcli_conf_json["sag"][key].append(line)
        return fmcli_conf_json 
    
    def get_running_configs(self, module):
        ansible_host = module.params.get('ansible_host', None)
        running_config_cmd = ["show run"]
        response = run_commands(module, running_config_cmd)
        # fmcli_conf = f"{ansible_host}_fmcli.cfg"
        # fmcli_json = f"{ansible_host}_fmcli.json"
        fmcli_conf = f"fmcli.cfg"
        fmcli_json = f"fmcli.json"
        with open(fmcli_conf, "w") as f:
            resp = "\n".join(response)
            f.write(resp)

        fmcli_conf_json = self.fmcli_config_to_json(fmcli_conf)
        
        with open(fmcli_json, "w") as json_f:
            json.dump(fmcli_conf_json, json_f, indent=4)
        
        return fmcli_conf_json