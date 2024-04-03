#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Peter Sprygada <psprygada@ansible.com>
# Copyright: (c) 2024, Aviz Networks

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import time

from ansible.module_utils._text import to_text
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.parsing import (
    Conditional,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    EntityCollection,
    to_lines,
)
from ansible_collections.aviznetworks.sonic_fmcli.plugins.module_utils.network.sonic.sonic import run_commands
from ansible_collections.aviznetworks.sonic_fmcli.plugins.module_utils.network.sonic.utils.utils import command_list_str_to_dict
from ansible_collections.aviznetworks.sonic_fmcli.plugins.module_utils.network.sonic.configs.bgp_address_family import BGPAddressFamilyConfig
from ansible_collections.aviznetworks.sonic_fmcli.plugins.module_utils.network.sonic.argspecification.bgp_address_family import BGPAddressFamilyArgs

def transform_commands_dict(module, commands_dict):
    transform = EntityCollection(
        module,
        dict(
            command=dict(key=True),
            output=dict(),
            prompt=dict(type="list"),
            answer=dict(type="list"),
            newline=dict(type="bool", default=True),
            sendonly=dict(type="bool", default=False),
            check_all=dict(type="bool", default=False),
        ),
    )

    return transform(commands_dict)


def parse_commands(module, warnings):
    commands_dict = command_list_str_to_dict(module, warnings, module.params["commands"])
    commands = transform_commands_dict(module, commands_dict)
    return commands


def main():
    """main entry point for module execution
    """
    module = AnsibleModule(argument_spec=BGPAddressFamilyArgs.argument_spec, supports_check_mode=True)
    
    # ansible_host = list(module.params.keys())
    # with open("fmcli_hosts_data.txt", "w") as f:
    #         ansible_host = ", ".join(ansible_host)
    #         f.write(ansible_host)
    # responses = run_commands(module, ["show run"])

    
    commands = list()
    commands.extend(BGPAddressFamilyConfig().get_config_commands(module, get_current_config=True))
    
    # commands.extend(['end', 'save'])
    # print(module.params['commands'])
    module.params['commands'] = commands

    result = {'changed': False}

    warnings = list()
    # print(f"commands: {module.params}")
    commands = parse_commands(module, warnings)
    result['warnings'] = warnings

    wait_for = module.params['wait_for'] or list()
    try:
        conditionals = [Conditional(c) for c in wait_for]
    except AttributeError as exc:
        module.fail_json(msg=to_text(exc))
    retries = module.params['retries']
    interval = module.params['interval']
    match = module.params['match']

    while retries > 0:
        responses = run_commands(module, commands)
        for item in list(conditionals):
            if item(responses):
                if match == 'any':
                    conditionals = list()
                    break
                conditionals.remove(item)

        if not conditionals:
            break

        time.sleep(interval)
        retries -= 1

    if conditionals:
        failed_conditions = [item.raw for item in conditionals]
        msg = 'One or more conditional statements have not been satisfied.'
        module.fail_json(msg=msg, failed_conditions=failed_conditions)

    result.update({
        'stdout': responses,
        'stdout_lines': list(to_lines(responses))
    })

    module.exit_json(**result)


if __name__ == '__main__':
    main()