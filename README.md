Ansible Collection by Aviz Networks India Pvt. Ltd. for Community/Enterprise SONiC Distribution 
=================================================================================

It includes Ansible core modules to provision and manage the Siwtch running Community/Enterprise SONiC Distribution. Sample playbooks and documentation are also included to show how the collection can be used.

Supported connections
---------------------
The SONiC Ansible collection supports network_cli connections over AVIZ ISCLI prompt.

Plugins
--------
**CLICONF plugin**

Name | Description
--- | ---
[network_cli](https://github.com/AvizNetworks/aviznetworks.sonic)|Use Ansible CLICONF to run commands on AVIZ ISCLI prompt in SONiC.
Supported operations are ***merge*** and ***delete***.


[**Collection core modules**](../aviznetworks.sonic/documents/AvizNetworks_ansible.md)
------------------------
| Name                         | Description                                                                    | Connection type |
|------------------------------|--------------------------------------------------------------------------------|-----------------|
| **sonic_commands**           | Execute list of commands under fmcli prompt                                    | network_cli     |
| **sonic_bgp**                | Manage global BGP and its parameters                                           | network_cli     |
| **sonic_bgp_address_family** | Manage global BGP address-family and its parameters                            | network_cli     |
| **sonic_bgp_neighbor**       | Manage a BGP neighbor and its parameters                                       | network_cli     |
| **sonic_bgp_route_maps**     | Manage route map configuration                                                 | network_cli     |
| **sonic_interfaces**         | Configure Interface attributes                                                 | network_cli     |
| **sonic_mlag**               | Manage multi chassis link aggregation groups domain (MCLAG) and its parameters | network_cli     |
| **sonic_vlan**               | Manage VLAN and its parameters                                                 | network_cli     |
| **sonic_port_channel**       | Manage portchannel and its parameters                                          | network_cli     |
| **sonic_loopback**           | Manage loopback and its parameters                                             | network_cli     |

Sample use case playbooks
-------------------------
The playbooks directory includes this sample playbook that show end-to-end use cases.

Version compatibility
----------------------
* Recommended Ansible version 2.14 or higher 
* Recommended Python 3.9 or higher


Installation of Ansible
-----------------------------
      pip3 install paramiko>=2.7
      pip3 install jinja2>=2.8
      pip3 install ansible-core

Download Ansible-collection
-----------------------------
[**Ansible-collection**](https://github.com/AvizNetworks/aviznetworks.sonic)


Setting Environment for the playbook execution
----------------------------------------------
Post downloading the ansible collection, open a terminal, change directory to aviznetworks.sonic and execute the command ***sudo sh rebuild.sh***

Sample playbooks
-----------------
**VLAN configuration**

***sonic_leaf1.yaml***

    ---
    - name: "FMCLI Ports Configuration "
      hosts: leaf01
      gather_facts: no
      connection: network_cli
      collections:
        - aviznetworks.sonic
      
      tasks:

        - name: "day-1 Add member port to port-channel configuration"
          sonic_port_channel:
            config:
              - pch_id: 10
                interfaces: ["Ethernet200"]
                description: "pch description"
                mode: "active"

        - name: "day-1 vlan trunk mode on pch and interfaces"
          sonic_vlan:
            config:
              - vlan_ids: [20, 30, 40]  # [20, 30, 35-37]
                vlan_mode: "trunk"
                interfaces: ["Ethernet200", "Ethernet208"]
                pch_ids: [10]



***hosts***

    [LEAF01]
    leaf01 ansible_host=10.20.8.15 ansible_user=admin ansible_ssh_pass=Innovium123 ansible_connection=network_cli ansible_network_os=aviznetworks.sonic_fmcli.sonic

    [LEAF02]
    leaf02 ansible_host=10.20.8.16 ansible_user=admin ansible_ssh_pass=Innovium123 ansible_connection=network_cli ansible_network_os=aviznetworks.sonic_fmcli.sonic

    [SPINE01]
    spine01 ansible_host=10.20.8.11 ansible_user=admin ansible_ssh_pass=Innovium123 ansible_connection=network_cli ansible_network_os=aviznetworks.sonic_fmcli.sonic

    [SPINE02]
    spine02 ansible_host=10.20.8.12 ansible_user=admin ansible_ssh_pass=Innovium123 ansible_connection=network_cli ansible_network_os=aviznetworks.sonic_fmcli.sonic

    [all:vars]
    # ansible_connection=ssh
    ansible_connection=network_cli
    ansible_user=admin
    ansible_ssh_pass=Innovium123
    # [datacenter:vars]
    ansible_network_os=aviznetworks.sonic_fmcli.sonic
    ansible_python_interpreter=/usr/bin/python3

    [alldevices:children]
    LEAF01
    LEAF02
    SPINE01
    SPINE02

    [allLEAFS:children]
    LEAF01
    LEAF02



***command to run***

    ansible-playbook playbooks/sonic_leaf1.yaml -i inventory/hosts -vvv