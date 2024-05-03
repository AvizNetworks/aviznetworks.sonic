from __future__ import absolute_import, division, print_function
__metaclass__ = type

import traceback
import json
import re

from ansible.module_utils._text import to_native

try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote

try:
    import jinja2
    HAS_LIB = True
except Exception as e:
    HAS_LIB = False
    ERR_MSG = to_native(e)
    LIB_IMP_ERR = traceback.format_exc()

from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.sonic import (
    to_request,
    edit_config
)
from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.utils.utils import (
    get_substring_starstwith_matched_item_list, 
    substring_starstwith_check)

def get_vlan_ids(module_config):
    # vlan_id: [10, 20, 100-110, 115, 117-120]
    vlan_id = []
    for item in module_config["vlan_ids"]:
        item = str(item)
        if "-" in item:
            item_split = item.split("-")
            for i in range(int(item_split[0]), int(item_split[1])+1):
                vlan_id.append(str(i))
        else:
            vlan_id.append(item)
    return vlan_id

def config_vlans(module_config, config_list, diff={}):
    # diff = {"vlan":{} , }
    commands = []
    vlan_ids = get_vlan_ids(module_config)
    
    for vlan_id in vlan_ids:
        key = f"vlan {vlan_id}"
        diff["vlan"][key] = []
        commands.append("config terminal")
        if key in config_list["vlan"]:
            if module_config.get("vrf_name"):
                cmd = f"vrf member {module_config['vrf_name']}"
                commands.append(key)
                if cmd in config_list["vlan"][key]:
                    commands = commands[:-1]
                    pass
                else:
                    if substring_starstwith_check("vrf member", config_list["vlan"]):
                        commands.append(cmd)
                        cmd_dlt = get_substring_starstwith_matched_item_list("vrf member", config_list["vlan"])
                        diff["vlan"][key].append(f"- {cmd_dlt}")
                        diff["vlan"][key].append(f"+ {cmd}")
                    else:
                        commands.append(cmd)
                        diff["vlan"][key].append(f"+ {cmd}")
            commands.extend(["end", "save"])
        else:     
            commands.append(key)
            diff["vlan"][key].append(f"+ {key}")
            if module_config.get("vrf_name"):
                cmd = f"vrf member {module_config['vrf_name']}"
                commands.append(cmd)
                diff["vlan"][key].append(f"+ {cmd}")    
            commands.extend(["end", "save"]) 
                
    return commands, diff

# def get_configured_vlan_members(config_list, vlan_id):
