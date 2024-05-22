#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2020, Peter Sprygada <psprygada@ansible.com>
# Copyright: (c) 2024, Aviz Networks

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: ports_configuration
version_added: 1.0.0
notes:
- Tested against Community SONiC Distribution.
- Supports C(check_mode).
short_description: Runs commands on devices running Community SONiC
description:
  - Runs commands on remote devices running Community SONiC Distribution. 
    Sends arbitrary commands to a SONiC node and
    returns the results that are read from the device. This module includes an
    argument that causes the module to wait for a specific condition
    before returning or time out if the condition is not met.
  - This module does not support running commands in configuration mode.
    To configure SONiC devices, use M(sonic_config).
options:
  commands:
    description:
      - List of commands to send to the remote Community SONiC devices over the
        configured provider. The resulting output from the command
        is returned. If the I(wait_for) argument is provided, the
        module is not returned until the condition is satisfied or
        the number of retries has expired. If a command sent to the
        device requires answering a prompt, it is possible to pass
        a dict containing I(command), I(answer) and I(prompt).
        Common answers are 'yes' or "\\r" (carriage return, must be
        double quotes). See examples.
    type: list
    elements: str
    required: true
  wait_for:
    description:
      - List of conditions to evaluate against the output of the
        command. The task waits for each condition to be true
        before moving forward. If the conditional is not true
        within the configured number of retries, the task fails.
        See examples.
    type: list
    elements: str
  match:
    description:
      - The I(match) argument is used in conjunction with the
        I(wait_for) argument to specify the match policy.  Valid
        values are C(all) or C(any). If the value is set to C(all)
        then all conditionals in the wait_for must be satisfied. If
        the value is set to C(any) then only one of the values must be
        satisfied.
    type: str
    default: all
    choices: [ 'all', 'any' ]
  retries:
    description:
      - Specifies the number of retries a command should be run
        before it is considered failed. The command is run on the
        target device every retry and evaluated against the
        I(wait_for) conditions.
    type: int
    default: 10
  interval:
    description:
      - Configures the interval in seconds to wait between retries
        of the command. If the command does not pass the specified
        conditions, the interval indicates how long to wait before
        trying the command again.
    type: int
    default: 1
"""

EXAMPLES = """
  - name: Runs show version on remote devices
    sonic_ports:
      interface: 'Ethernet36'
      description: "fmcli description_eth36"
      wait_for:
        - result[4] contains "Saving Configuration"
"""

RETURN = """
stdout:
  description: The set of responses from the commands.
  returned: always apart from low level errors (such as action plugin)
  type: list
  sample: ['...', '...']
stdout_lines:
  description: The value of stdout split into a list.
  returned: always apart from low level errors (such as action plugin)
  type: list
  sample: [['...', '...'], ['...'], ['...']]
failed_conditions:
  description: The list of conditionals that have failed.
  returned: failed
  type: list
  sample: ['...', '...']
warnings:
  description: The list of warnings (if any) generated by module based on arguments.
  returned: always
  type: list
  sample: ['...', '...']
"""
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
from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.sonic import run_commands
from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.utils.utils import \
    command_list_str_to_dict
from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.configs.mlag import MLAGConfig
from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.argspecification.mlag import MlagArgs


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


def parse_commands(module, warnings, commands):
    commands_dict = command_list_str_to_dict(module, warnings, commands)
    commands = transform_commands_dict(module, commands_dict)
    return commands


def main():
    """main entry point for module execution
    """
    module = AnsibleModule(argument_spec=MlagArgs.argument_spec, supports_check_mode=True)

    ansible_host = list(module.params.keys())
    with open("fmcli_hosts_data.txt", "w") as f:
        ansible_host = ", ".join(ansible_host)
        f.write(ansible_host)
    responses = run_commands(module, ["show run"])

    commands, diff = MLAGConfig().get_config_commands(module, get_current_config=True)

    module.params['commands'] = commands
    module.params['diff'] = diff

    result = {'changed': False}

    warnings = list()
    commands = parse_commands(module, warnings, commands)
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
