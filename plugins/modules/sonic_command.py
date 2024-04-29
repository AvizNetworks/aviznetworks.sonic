#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Peter Sprygada <psprygada@ansible.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = """
---
module: sonic_command
version_added: 1.0.0
notes:
- Tested against Enterprise SONiC Distribution.
- Supports C(check_mode).
author: Dhivya P (@dhivayp)
short_description: Runs commands on devices running Enterprise SONiC
description:
  - Runs commands on remote devices running Enterprise SONiC Distribution.
    Sends arbitrary commands to an Enterprise SONiC node and
    returns the results that are read from the device. This module includes an
    argument that causes the module to wait for a specific condition
    before returning or time out if the condition is not met.
  - This module does not support running commands in configuration mode.
    To configure SONiC devices, use M(aviznetworks.sonic.sonic_config).
options:
  commands:
    description:
      - List of commands to send to the remote Enterprise SONiC devices over the
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
    aviznetworks.sonic.sonic_command:
      commands: show version

  - name: Runs show version and checks to see if output contains 'Aviz'
    aviznetworks.sonic.sonic_command:
      commands: show version
      wait_for: result[0] contains Aviz

  - name: Runs multiple commands on remote nodes
    aviznetworks.sonic.sonic_command:
      commands:
        - show version
        - show interface

  - name: Runs multiple commands and evaluate the output
    aviznetworks.sonic.sonic_command:
      commands:
        - 'show version'
        - 'show system'
      wait_for:
        - result[0] contains Aviz
        - result[1] contains Hostname

  - name: Runs commands that require answering a prompt
    aviznetworks.sonic.sonic_command:
      commands:
        - command: 'reload'
          prompt: '[confirm yes/no]: ?$'
          answer: 'no'
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
import re, json

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
from ansible_collections.aviznetworks.sonic.plugins.module_utils.network.sonic.utils.utils import command_list_str_to_dict


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

def fmcli_config_to_json(fmcli_conf, fmcli_json):
    # with open("fmcli_db.config", "w") as f:
    #         resp = "\n".join(responses)
    #         f.write(resp)
    fmcli_conf = "10.4.4.66_fmcli_db.config"
    fmcli_json = "10.4.4.66_fmcli_db.json"
    fmcli_conf_json = {}
    fmcli_conf_json["vlan"] = []
    # fmcli_conf_json["interface"] = {"port-channel":{}, "ethernet": {}, "lo": {}, "vlan":{}}
    fmcli_conf_json["interface"] = {}
    key = ""

    with open(fmcli_conf, "r") as fmcli:
        fmcli_conf_lines = fmcli.readlines()

    for count, line in enumerate(fmcli_conf_lines):
        line = line.strip()
        if line == "!":
            # config_start = True
            interface_config = False
            key = ""
        else:
            # vlan json data
            if re.match("^vlan\s\d+$", line):
                fmcli_conf_json["vlan"].append(int(line.split()[1]))
            
            # interface ethernet | vlan | lo | port-channel json data
            elif interface_config or re.match("^interface\s(vlan|lo|port-channel|ethernet)\s\S+", line):
                interface_config = True
                if not key:
                    key = line
                    if key not in fmcli_conf_json["interface"]:
                        fmcli_conf_json["interface"][line] = []
                else:
                    fmcli_conf_json["interface"][key].append(line)

    with open(fmcli_json, "w") as json_file:
        json.dump(fmcli_conf_json, json_file, indent=4)
                    



def main():
    """main entry point for module execution
    """
    argument_spec = dict(
        # { command: <str>, prompt: <str>, response: <str> }
        commands=dict(type='list', required=True, elements="str"),

        wait_for=dict(type='list', elements="str"),
        match=dict(default='all', choices=['all', 'any']),

        retries=dict(default=10, type='int'),
        interval=dict(default=1, type='int')
    )

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)
    result = {'changed': False}

    warnings = list()
#    check_args(module, warnings)
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
        with open("fmcli_db.config", "w") as f:
            resp = "\n".join(responses)
            f.write(resp)
            
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
