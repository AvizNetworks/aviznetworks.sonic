
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

intf_speed_map = {
    0: 'SPEED_DEFAULT',
    10: "SPEED_10MB",
    100: "SPEED_100MB",
    1000: "SPEED_1GB",
    2500: "SPEED_2500MB",
    5000: "SPEED_5GB",
    10000: "SPEED_10GB",
    20000: "SPEED_20GB",
    25000: "SPEED_25GB",
    40000: "SPEED_40GB",
    50000: "SPEED_50GB",
    100000: "SPEED_100GB",
    200000: "SPEED_200GB",
    400000: "SPEED_400GB",
    800000: "SPEED_800GB"
}

def config_autoneg(module_config, config_list, diff={}, key=""):
    commands = []
    cmd = f"autoneg enable"
    if cmd in config_list:
        pass
    elif cmd not in config_list:
        commands.append(f"autoneg enable")
        diff["interfaces"][key].append(f"+ {cmd}")
    elif module_config['autoneg'] is False:
        cmd = f"autoneg enable"
        if cmd in config_list:
            commands.append(f"no autoneg enable")
            diff["interfaces"][key].append(f"- {cmd}")
    return commands, diff

def config_ip_address(module_config, config_list, diff={}, key=""):
    commands = []
    cmd = f"ip address {module_config['ip_address']}"
    if cmd in config_list:
        pass
    elif substring_starstwith_check("ip address", config_list):
        cmd_dlt = get_substring_starstwith_matched_item_list("ip address", config_list)
        commands.append(f"no {cmd_dlt}")
        commands.append(cmd)
        diff["interfaces"][key].append(f"- {cmd_dlt}")
        diff["interfaces"][key].append(f"+ {cmd}")
    else:
        commands.append(cmd)
        diff["interfaces"][key].append(f"+ {cmd}")
        
    return commands, diff

def config_mtu(module_config, config_list, diff={}, key=""):
    commands = []
    cmd = f"mtu {module_config['mtu']}"
    if cmd in config_list:
        pass
    elif substring_starstwith_check("mtu", config_list):
        cmd_dlt = get_substring_starstwith_matched_item_list("mtu", config_list)
        commands.append(cmd)
        diff["interfaces"][key].append(f"- {cmd_dlt}")
        diff["interfaces"][key].append(f"+ {cmd}")
    else:
        commands.append(cmd)
        diff["interfaces"][key].append(f"+ {cmd}")
        
    return commands, diff

def config_speed(module_config, config_list, diff={}, key=""):
    commands = []
    cmd = f"speed {module_config['speed']}"
    if cmd in config_list:
        pass
    elif substring_starstwith_check("speed", config_list):
        cmd_dlt = get_substring_starstwith_matched_item_list("speed", config_list)
        commands.append(cmd)
        diff["interfaces"][key].append(f"- {cmd_dlt}")
        diff["interfaces"][key].append(f"+ {cmd}")
    else:
        commands.append(cmd)
        diff["interfaces"][key].append(f"+ {cmd}")
        
    return commands, diff

def config_description(module_config, config_list, diff=None, key=""):
    if diff is None:
        diff = {}
    commands = []
    cmd = f"description {module_config['description']}"
    if cmd in config_list:
        pass
    elif substring_starstwith_check("description", config_list):
        cmd_dlt = get_substring_starstwith_matched_item_list("description", config_list)
        commands.append(cmd)
        diff["interfaces"][key].append(f"- {cmd_dlt}")
        diff["interfaces"][key].append(f"+ {cmd}")
    else:
        commands.append(cmd)
        diff["interfaces"][key].append(f"+ {cmd}")
        
    return commands, diff

def config_fec(module_config, config_list, diff={}, key=""):
    commands = []
    cmd = f"forward-error-correction {module_config['fec']}"
    if cmd in config_list:
        pass
    elif substring_starstwith_check("forward-error-correction", config_list):
        cmd_dlt = get_substring_starstwith_matched_item_list("forward-error-correction", config_list)
        commands.append(cmd)
        diff["interfaces"][key].append(f"- {cmd_dlt}")
        diff["interfaces"][key].append(f"+ {cmd}")
    else:
        commands.append(cmd)
        diff["interfaces"][key].append(f"+ {cmd}")
        
    return commands, diff

def config_channel_group(module_config, config_list, diff={}, key=""):
    # diff = diff["interfaces"][key] // parameter diff
    commands = []
    if module_config['mode'] == "active":
        cmd = f"channel-group {module_config['pch_id']} mode {module_config['mode']}"
        if cmd in config_list:
            pass
        elif substring_starstwith_check("channel-group", config_list):
            cmd_dlt = get_substring_starstwith_matched_item_list("channel-group", config_list)
            commands.append(f"no {cmd_dlt}")
            commands.append(cmd)
            diff["interfaces"][key].append(f"- {cmd_dlt}")
            diff["interfaces"][key].append(f"+ {cmd}")
        else:
            commands.append(cmd)
            diff["interfaces"][key].append(f"+ {cmd}")
    elif substring_starstwith_check("channel-group", config_list):
            cmd_dlt = get_substring_starstwith_matched_item_list("channel-group", config_list)
            commands.append(f"no {cmd_dlt}")
            diff["interfaces"][key].append(f"- {cmd_dlt}")
    return commands , diff

def get_portchannel_member_interfaces(running_interface_config, pch_id):
    # running_interface_config = running_config["interface"]
    
    interfaces = []
    intf_keys = list(running_interface_config.keys())
    for intf in intf_keys:
        config_list = running_interface_config.get(intf)
        interface_cg = get_substring_starstwith_matched_item_list("channel-group", config_list)
        if f" {str(pch_id)} " in interface_cg:
            interfaces.append(intf.split()[-1])
    return interfaces


# To create Loopback, VLAN interfaces
def build_interfaces_create_request(interface_name):
    url = "data/openconfig-interfaces:interfaces"
    method = "PATCH"
    payload_template = """{"openconfig-interfaces:interfaces": {"interface": [{"name": "{{interface_name}}", "config": {"name": "{{interface_name}}"}}]}}"""
    input_data = {"interface_name": interface_name}
    env = jinja2.Environment(autoescape=False)
    t = env.from_string(payload_template)
    intended_payload = t.render(input_data)
    ret_payload = json.loads(intended_payload)
    request = {"path": url,
               "method": method,
               "data": ret_payload}
    return request


def retrieve_port_group_interfaces(module):
    port_group_interfaces = []
    method = "get"
    port_num_regex = re.compile(r'[\d]{1,4}$')
    port_group_url = 'data/openconfig-port-group:port-groups'
    request = {"path": port_group_url, "method": method}
    try:
        response = edit_config(module, to_request(module, request))
    except ConnectionError as exc:
        module.fail_json(msg=str(exc), code=exc.code)

    if 'openconfig-port-group:port-groups' in response[0][1] and "port-group" in response[0][1]['openconfig-port-group:port-groups']:
        port_groups = response[0][1]['openconfig-port-group:port-groups']['port-group']
        for pg_config in port_groups:
            if 'state' in pg_config:
                member_start = pg_config['state'].get('member-if-start', '')
                member_start = re.search(port_num_regex, member_start)
                member_end = pg_config['state'].get('member-if-end', '')
                member_end = re.search(port_num_regex, member_end)
                if member_start and member_end:
                    member_start = int(member_start.group(0))
                    member_end = int(member_end.group(0))
                    port_group_interfaces.extend(range(member_start, member_end + 1))

    return port_group_interfaces


def retrieve_default_intf_speed(module, intf_name):

    # Read the valid_speeds
    dft_intf_speed = 'SPEED_DEFAULT'
    method = "get"
    sonic_port_url = 'data/sonic-port:sonic-port/PORT/PORT_LIST=%s'
    sonic_port_vs_url = (sonic_port_url + '/valid_speeds') % quote(intf_name, safe='')
    request = {"path": sonic_port_vs_url, "method": method}
    try:
        response = edit_config(module, to_request(module, request))
    except ConnectionError as exc:
        module.fail_json(msg=str(exc), code=exc.code)
    if 'sonic-port:valid_speeds' in response[0][1]:
        v_speeds = response[0][1].get('sonic-port:valid_speeds', '')
        v_speeds_list = v_speeds.split(",")
        v_speeds_int_list = []
        for vs in v_speeds_list:
            v_speeds_int_list.append(int(vs))

        dft_speed_int = 0
        if v_speeds_int_list:
            dft_speed_int = max(v_speeds_int_list)
        dft_intf_speed = intf_speed_map.get(dft_speed_int, 'SPEED_DEFAULT')

    if dft_intf_speed == 'SPEED_DEFAULT':
        module.fail_json(msg="Unable to retireve default port speed for the interface {0}".format(intf_name))

    return dft_intf_speed
