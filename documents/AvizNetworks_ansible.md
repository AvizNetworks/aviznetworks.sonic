***********Ansible Module aviznetworks.sonic***********
=======================================================


________________________________________________________
________________________________________________________


# Day-2...day-n configuration difference

    In the Ansible script tasks, the `aviznetworks.sonic` module will check and compare the configuration of each task with the existing configuration on the devices. The module will merge the configurations if a similar configuration supports the protocol rules, or the new configurations will override it.

### Example:

**&nbsp;&nbsp;&nbsp;&nbsp; Day-1 Configuration**

    - name: SONiC port configuration
      sonic_interfaces:
         config:
             - interfaces: ["Ethernet32", "Ethernet4"]
               mtu: 9000
               enable: True

**&nbsp;&nbsp;&nbsp;&nbsp; Day-2 Configuration**
    
    - name: SONiC port configuration
      sonic_interfaces:
         config:
             - interfaces: ["Ethernet32"]
               mtu: 9100
               enable: True
               description: "fmcli description_eth32"
    

    In the example above, on `day-2 ... days-n` configuration, updating the MTU and configure 
the port description. In the log, `Diff` shows, removing the old mtu value and adding the new value. 
Only **description** getting added, because in the old configuration description was not provided.



### &nbsp;&nbsp;&nbsp;&nbsp;log:

    "diff": {
                "interfaces": {
                    "interface ethernet Ethernet32": [
                        "- mtu 9000",
                        "+ mtu 9100",
                        "+ description fmcli description_eth32",
                    ]
                }
            }

________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

# State: Merge / Delete

Two State supports will `merge/delete` the configuration on `day-0 ... day-n` task operation.

## **&nbsp;&nbsp;1. Merge**
     A default operation, will be used in case of `merge/add/update/override` 
configurations.

    # day-0

    - name: SONiC port configuration
      sonic_interfaces:
         config:
             - interfaces: ["Ethernet32"]
               mtu: 9000
               enable: True
               description: "fmcli description_eth32"
        
             - interfaces: ["Ethernet34"]
               mtu: 9000
               description: "fmcli description_eth34"
    
    
       state: merge  # default
    
    ____________________________________________________________________________________________________________________
    
    # day-n  
    
    - name: SONiC port configuration
      sonic_interfaces:
         config:
             - interfaces: ["Ethernet32"]
               mtu: 9000
               ip_address: 40.0.0.10/31 # new configuration
               description: "fmcli description_eth32"
         state: merge  # default


     In this configuration, it will check if any configuration exists it will get overridden and if 
it does not exist it will get added as a new configuration.

### &nbsp;&nbsp;&nbsp;&nbsp;log:
    # Day-0 

    "commands": [
            "config terminal",
            "interface ethernet Ethernet32",
            "mtu 9000",
            "no shutdown",
            "description fmcli description_eth32",
            "end",
            "save",
            "config terminal",
            "interface ethernet Ethernet34",
            "mtu 9000",
            "description fmcli description_eth32",
            "end",
            "save"
        ]

    ____________________________________________________________________________________________________________________ 
    
    # Day-n

    "commands": [
            "config terminal",
            "interface ethernet Ethernet32",
            "ip address 40.0.0.2/31",
            "end",
            "save"
        ]

## **&nbsp;&nbsp;2. Delete**

    It will delete the configuration if it already exists.
    
   ### ***&nbsp;&nbsp;&nbsp;&nbsp;a) Delete inner configs***
    # day-0

    - name: SONiC port configuration
      sonic_interfaces:
         config:
             - interfaces: ["Ethernet32", "Ethernet36"]
               mtu: 9000
               enable: True
               description: "fmcli description"
         state: merge  # default

    ____________________________________________________________________________________________________________________

    # day-n delete some config. Ex: delete the description for the interfaces

    - name: SONiC port configuration
      sonic_interfaces:
           config:
             - interfaces: ["Ethernet32", "Ethernet36"]
               description: "fmcli description"
           state: delete

    Here, `day-n` task will delete the inner configuration only mentioned under the interface.

### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;log:
    # Day-0 

    "commands": [
            "config terminal",
            "interface ethernet Ethernet32",
            "mtu 9000",
            "no shutdown",
            "description fmcli description",
            "end",
            "save",
            "config terminal",
            "interface ethernet Ethernet36",
            "mtu 9000",
            "no shutdown",
            "description fmcli description",
            "end",
            "save"
        ]

    ____________________________________________________________________________________________________________________ 
    
    # Day-n

    "commands": [
            "config terminal",
            "interface ethernet Ethernet32",
            "no description fmcli description",
            "end"
            "save",
            "config terminal",
            "interface ethernet Ethernet36",
            "no description fmcli description",
            "end"
            "save"
        ]


   ### ***&nbsp;&nbsp;&nbsp;&nbsp;b) Delete whole configs***
    # day-0, day-1, ...

    - name: SONiC port configuration
      sonic_interfaces:
           config:
             - interfaces: ["Ethernet32", "Ethernet36"]
               mtu: 9000
               enable: True
               description: "fmcli description"


    ____________________________________________________________________________________________________________________
    # day-n delete whole config 

    - name: SONiC port configuration
        sonic_interfaces:
            config:
              - interfaces: ["Ethernet32", "Ethernet36"]
            state: delete  

     Here, `day-n` task will delete the complete configuration for the listed interfaces


### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;log:
    # Day-0 

    "commands": [
            "config terminal",
            "interface ethernet Ethernet32",
            "mtu 9000",
            "no shutdown",
            "description fmcli description",
            "end",
            "save",
            "config terminal",
            "interface ethernet Ethernet36",
            "mtu 9000",
            "no shutdown",
            "description fmcli description",
            "end",
            "save"
        ]

    ____________________________________________________________________________________________________________________ 
    
    # Day-n

    "commands": [
            "config terminal",
            "interface ethernet Ethernet32",
            "no mtu 9000",
            "shutdown",
            "no description fmcli description",
            "end"
            "save",
            "config terminal",
            "no interface ethernet Ethernet32",
            "end"
            "save",
            "config terminal",
            "interface ethernet Ethernet36",
            "no mtu 9000",
            "shutdown",
            "no description fmcli description",
            "end"
            "save",
            "config terminal",
            "no interface ethernet Ethernet36",
            "end"
            "save"
        ]

________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

# Ports/Interface
    Configuring and deleting multiple interfaces.

    Executes the task with the module `sonic_interfaces`. Provide the configuration
data as a list under the “**config**” key. Here “**interface**” is the primary key.

**&nbsp;&nbsp;&nbsp;&nbsp; Supported keys/arguments - value:**

| key         | description                                                                                                                                                                       |
|-------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| interfaces  | - a primary key argument<br>- list of interface names. **Ex:** ["Ethernet32", "Ethernet4"]                                                                                        |
| mtu         | - mtu value, int type. **Ex:** 9100                                                                                                                                               |
| enable      | - To enable or disable the ports, boolean type. **Ex:** true/false <br> **true**: enable/bring-up the ports <br> **false**: disable/bring-down the ports                          |
| ip_address  | - Configure the IP(v4) address to a port. <br> - provide the IP address with a mask. **Ex:** 10.4.4.4/24 <br> - make sure, use a single interface name for the argument interface |
| description | - Description of interfaces                                                                                                                                                       |
| fec         | - forward-error-correction <br> - Choose a value from the list: `["rs", "fc", "none"]`                                                                                            |
| speed       | - Choose a value from the list:`["1G", "10G", "25G", "40G", "50G", "100G", "400G"]`                                                                                               |

**&nbsp;&nbsp;&nbsp;&nbsp; Sample playbook task**

      - name: SONiC port configuration
        sonic_interfaces:
           config:
               - interface: ["Ethernet32", "Ethernet4"]
                 mtu: 9000
                 enable: true
                 description: "fmcli description_port"
               - interface: 'Ethernet36'
                 mtu: 9000
                 fec: rs
                 enable: false
                 ip_address: 10.4.4.4/23
                 description: "fmcli description"


________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

# Loopback
    A loopback interface is a virtual Layer 3 interface. A loopback interface emulates a physical interface and is always 
in the UP state.

    To configure and delete multiple loopbacks, execute the task with the module 
`sonic_loopback`. Provide the configuration data as a list under the “**config**” key. Here “**loopback_id*” is the 
primary key.

**&nbsp;&nbsp;&nbsp;&nbsp; Supported keys/arguments - value:**

| key         | description                                                                                                         |
|-------------|---------------------------------------------------------------------------------------------------------------------|
| loopback_id | - a primary key argument<br>- int type. **Ex:** 1                                                                   |
| ip_address  | - Configure the IP(v4) address to an Interface. <br> - provide the IP address with a mask. **Ex:** 10.4.4.4/24 <br> |

**&nbsp;&nbsp;&nbsp;&nbsp; Sample playbook task**

      # task 1: add or merge the loopback configuration
      - name: SONiC loopback configuration merge
        sonic_loopback:
             config:
               - loopback: 1
                 ip_address: 10.4.5.8/23
               - loopback: 2
                 ip_address: 10.4.5.7/23
      
    ____________________________________________________________________________________________________________________
    
     # task 2: delete the loopback 1 configuration
     - name: SONiC loopback configuration delete
       sonic_loopback:
            config:
               - loopback: 1
                 state: delete # delete loopback 1
      
    ____________________________________________________________________________________________________________________      
      
     # task 3: delete the ip_address from loopback 2 configuration
     - name: SONiC loopback configuration delete
       sonic_loopback:
            config:
               - loopback: 2
                 ip_address: 10.4.5.7/23
            state: delete # delete ip_address from loopback 2
      
    ____________________________________________________________________________________________________________________
      
     # task 4: delete the loopback 1 and loopback 2 configuration
     - name: SONiC loopback configuration delete
       sonic_loopback:
            config:
               - loopback: 1
               - loopback: 2
                 ip_address: 10.4.5.7/23
            state: delete # delete loopback 1 and ip_address from loopback 2


________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

# Vlan
    Configure and delete multiple vlans.

    The switch supports up to `4094` VLANs. Each can be identified with a number 
between 2 and 4094.

    To configure Vlans execute the task with the module `sonic_vlan`. Provide the 
configuration data as a list under the “**config**” key. Here “**vlan_ids**” is the primary key.

**&nbsp;&nbsp;&nbsp;&nbsp; Supported keys/arguments - value:**

| key             | description                                                                                                                                                                                                                                                                                                                      |
|-----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| vlan_ids        | - a primary key argument<br>- list of Vlan id. **Ex:** ["100", "200", "221-223"] <br> - Vlan id can be in range. Ex: ["221-223"]<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; # It will create the VLAN ids 221, 222, 223 |
| vlan_id         | - a primary key argument<br>- a single Vlan id. Ex: "100"<br>**Note:** use either `vlan_ids` or `vlan_id`                                                                                                                                                                                                                        |
| interfaces      | - list of interface names and or list of portchannel id. **Ex:** ["Ethernet32", "Ethernet4", "portchannel10", "pch20"]                                                                                                                                                                                                           |
| vlan_mode       | - Vlan mode could be trunk or access<br>- Default vlan_mode is access mode<br>- When using access mode, the task will be executed only with the first **interface** from the list                                                                                                                                                |
| anycast_gateway | - The command sequence configures an anycast gateway IP address for a specific VLAN interface<br>- provide the IP address with a mask. **Ex:** 10.4.4.4/24<br>- Task will configure the IP address only on the first `vlan_ids` from the list or can be used `vlan_id`                                                           |
| ip_address      | - SVI(Switch Virtual Interface)<br>- Configure the IP address to the Vlan.<br>- provide the IP address with a mask. **Ex:** 10.4.4.4/24<br>- Task will configure the IP address only on the first `vlan_ids` from the list or can be used `vlan_id`                                                                              |

**&nbsp;&nbsp;&nbsp;&nbsp; Sample playbook task**

      - name: "vlan trunk mode on interfaces"
        sonic_vlan:
            config:
               - vlan_ids: [20, 30, 35-37]  # [20, 30, 35, 36, 37]
                 vlan_mode: "trunk"
                 interfaces: ["Ethernet200", "Ethernet208"]
      
    ____________________________________________________________________________________________________________________

      - name: "vlan access mode on interfaces"
        sonic_vlan:
            config:
               - vlan_id: 50
                 vlan_mode: "access"
                 interfaces: ["Ethernet204"]
      
    ____________________________________________________________________________________________________________________

      - name: "vlan trunk mode on portchannel"
        sonic_vlan:
            config:
               - vlan_ids: [20, 30, 40]  # [20, 30, 35-37]
                 vlan_mode: "trunk"
                 interfaces: ["portchannel300", "pch200"]
      
    ____________________________________________________________________________________________________________________      
      
      - name: "vlan ip_address configuration"
        sonic_vlan:
            config:
               - vlan_ids: [20]  #make sure provide one vlan id for SVI
                 ip_address: "100.10.0.5/25"

________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

# Portchannel
    Configure and delete multiple port-channel.

    To configure port-channel, execute the task with the module 
`sonic_port_channel`. Provide the configuration data as a list under the “**config**” key. Here “**pch_id**” is 
the primary key.

**&nbsp;&nbsp;&nbsp;&nbsp; Supported keys/arguments - value:**

| key         | description                                                                                                                                                                                                                                                                            |
|-------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| pch_id      | - a primary key argument<br>- portchannel id. **Ex:** "100"                                                                                                                                                                                                                            |
| interfaces  | - list of member interface names. **Ex:** ["Ethernet32", "Ethernet4"]                                                                                                                                                                                                                  |
| description | - portchannel description                                                                                                                                                                                                                                                              |
| mode        | - only supported value for the mode is "**active**"<br>- with active mode, it will configure the channel group or add members to the portchannel<br>- if mode argument not passed, it will not configure the members to the portchannel or remove the members from the portchannel<br> |

**&nbsp;&nbsp;&nbsp;&nbsp; Sample playbook task**

      - name: "create a port-channel"
        sonic_port_channel:
            config:
               - pch_id: 100
      
    ____________________________________________________________________________________________________________________

      - name: "Add member port to port-channel"
        sonic_port_channel:
            config:
               - pch_id: 200
                 interfaces: ["Ethernet216"]
                 description: "pch description 100"
                 mode: "active"

________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

# BGP
## &nbsp;&nbsp;1. BGP router
    To configure the BGP router, execute the task with the module `sonic_bgp`.
Provide the configuration data as a list under the “**config**” key. Here “**bgp_asn**” is the primary key.

A BGP configuration data list should be under the key “**bgp**”.

**&nbsp;&nbsp;&nbsp;&nbsp; Supported keys/arguments - value:**

| key                                                   | description                                                                                                                                                                                                                                                                                                                                                |
|-------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| bgp_asn                                               | - a primary key argument<br>- Configures BGP for an autonomous system (AS) number<br>- bgp as_number. **Ex:** "1001"                                                                                                                                                                                                                                       |
| bgp:<br>&nbsp;&nbsp;&nbsp;&nbsp; router_id            | - 32-bit IPv4 address to establish the peering session with bgp peers<br>- router id. Ex: 10.10.10.2                                                                                                                                                                                                                                                       |
| bgp:<br>&nbsp;&nbsp;&nbsp;&nbsp; bestpath             | - bestpath boolean type, **true** or **false**<br>- handle the paths received from different autonomous systems for multipath if their AS-path lengths are the same and all other multipath conditions are met<br>- allows load sharing across providers with different (but equal length) AS paths<br>- command: **bgp bestpath as-path multipath-relax** |
| bgp:<br>&nbsp;&nbsp;&nbsp;&nbsp; ebgp_requires_policy | - epbg_requires_policy boolean type, **true** or **false**<br>- default value is false<br>- restricts in and out policy requirements for BGP peers<br>- command: **bgp ebgp-requires-policy**<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; : **no bgp ebgp-requires-policy**                  |
| bgp:<br>&nbsp;&nbsp;&nbsp;&nbsp; restart_time         | - configure bgp graceful restart with restart-time in second<br>- **Ex:** 10<br>- command: **bgp graceful-restart restart-time 10**                                                                                                                                                                                                                        |
| bgp:<br>&nbsp;&nbsp;&nbsp;&nbsp; stalepath_time       | - configure bgp graceful restart with stalepath-time in second<br>- **Ex:** 10<br>- command: **bgp graceful-restart stalepath-time 10**                                                                                                                                                                                                                    |


**&nbsp;&nbsp;&nbsp;&nbsp; Sample playbook task**

      - name: Sonic BGP router config
        sonic_bgp:
            config:
               bgp_asn: 1001
               bgp:
                  - router_id: 10.10.10.2
                    ebgp_requires_policy: false
                    bestpath: true

________________________________________________________________________________________________________________________
## &nbsp;&nbsp;2. bgp_neighbors(IPv4)
    To configure the bgp_neighbors, execute the task with the module 
`sonic_bgp_neighbor`. Provide the configuration data as a list under the “**config**” key. Here “**bgp_asn**” is the 
primary key.

bgp_neighbor ipv4 configuration data list should be under the key “**neighbor: ipv4:**”.

**&nbsp;&nbsp;&nbsp;&nbsp; Supported keys/arguments - value:**

| key                                                                                                              | description                                                                                                                                                                                   |
|------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| bgp_asn                                                                                                          | - a primary key argument<br>- Configures BGP for an autonomous system (AS) number<br>- bgp as_number. **Ex:** "1001"                                                                          |
| neighbor:<br>&nbsp;&nbsp;&nbsp;&nbsp; ipv4:<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ips              | - 32-bit IPv4 address to establish the peering session with bgp peers<br>- router id. **Ex:** ["10.10.10.2", "10.10.10.3"]                                                                    |
| neighbor:<br>&nbsp;&nbsp;&nbsp;&nbsp; ipv4:<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; remote_as        | - Configure neighbor remote AS. **Ex:** 1002<br>- Two BGP routers become peers or neighbors once you establish a TCP connection b/w them<br>- command: **neighbor 10.10.10.2 remote-as 1002** |
| neighbor:<br>&nbsp;&nbsp;&nbsp;&nbsp; ipv4:<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; extended_nexthop | - extended next-hop boolean type, **true** or **false**<br>- default value is false<br>- Shutdown the BGP neighbor<br>- command: **neighbor 10.10.10.2 capability extended-nexthop**          |


**&nbsp;&nbsp;&nbsp;&nbsp; Sample playbook task**

      - name: Sonic BGP neighbor config
        sonic_bgp_neighbor:
            config:
               - bgp_asn: 1001
                 neighbor:
                     ipv4:
                        ips: ['40.0.0.2','40.0.0.10']
                        remote_as: 1002
                        extended_nexthop: true

________________________________________________________________________________________________________________________

## &nbsp;&nbsp;3. bgp_route_maps
    To configure bgp route maps, execute the task with the module 
`sonic_bgp_route_maps`. Provide the configuration data as a list under the “**config**” key. Here “**map_name**” 
is the primary key.

**&nbsp;&nbsp;&nbsp;&nbsp; Supported keys/arguments - value:**

| key                                 | description                                                                                            |
|-------------------------------------|--------------------------------------------------------------------------------------------------------|
| map_name                            | - a primary key argument<br>- Configures BGP route map<br>- map_name. **Ex:** "RM_SET_SRC"             |
| action                              | - action should be `permit` with **sequence_num**<br>- command: **route-map RM_SET_SRC permit 10**     |
| sequence_num                        | - configure route map sequence number<br>- **Ex:** 10<br>- command: **route-map RM_SET_SRC permit 10** |
| set:<br>&nbsp;&nbsp;&nbsp;&nbsp; ip | - set the source ip<br>- command: **set src 10.10.10.2**                                               |


**&nbsp;&nbsp;&nbsp;&nbsp; Sample playbook task**

      - name: Sonic route map config
        sonic_bgp_route_maps:
            config:
               - map_name: "RM_SET_SRC"
                 action: permit
                 sequence_num: 10   
                 set:
                    ip: 10.10.10.2

________________________________________________________________________________________________________________________
## &nbsp;&nbsp;4. bgp_address_family
    To configure bgp address family, execute the task with the module 
`sonic_bgp_address_family`. Provide the configuration data as a list under the “**config**” key. Here “**bgp_asn**” is 
the primary key.

**&nbsp;&nbsp;&nbsp;&nbsp; Supported keys/arguments - value:**

| key                                                                                     | description                                                                                                                                                                                                                                                                                                                                                                                                        |
|-----------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| bgp_asn                                                                                 | - a primary key argument<br>- Configures BGP for an autonomous system (AS) number<br>- bgp as_number. **Ex:** "1001"                                                                                                                                                                                                                                                                                               |
| address_family:<br>. . ipv4:<br>. . . . ips                                             | - 32-bit IPv4 address to establish the peering session with bgp peers<br>- router id. **Ex:** ["10.10.10.2", "10.10.10.3"]                                                                                                                                                                                                                                                                                         |
| address_family:<br>. . ipv4:<br>. . . . neighbor:<br>. . . . . . allowas_in             | - Accept as-path with my AS present in it<br>- This command is used to allow the BGP peer group to receive updates from neighboring autonomous systems (AS) with a different origin AS than the local AS, providing greater flexibility in accepting BGP routes<br>- value accepted for the argument “**allowas_in**” is **origin** or b/w **1-10**<br>- command: **neighbor 10.10.10.2 allowas-in 1**             |
| address_family:<br>. . ipv4:<br>. . . . neighbor:<br>. . . . . . route_reflector_client | - Configure a neighbor as Route Reflector client<br>- boolean type, **true** or **false**<br>- command: **neighbor 40.0.0.11 route-reflector-client**                                                                                                                                                                                                                                                              |
| address_family:<br>. . ipv4:<br>. . . . neighbor:<br>. . . . . . next_hop_self          | - Next hop<br>- Set local router as next-hop for routes received from the peer group, affecting routing within the autonomous system (AS). Optional "force" modifies next-hop for eBGP-learned routes<br>- boolean type, **true** or **false**<br>- command: **neighbor 40.0.0.11 next-hop-self force**                                                                                                            |
| address_family:<br>. . ipv4:<br>. . . . network                                         | - Configures an IP v4 prefix for advertisement<br>- IPv4 Address - Router IP address with masklen<br>- **Ex:** ["10.10.10.2/31", "10.10.10.3/31"]<br>- command: **network 10.10.10.2/31**                                                                                                                                                                                                                          |
| address_family:<br>. . ipv4:<br>. . . . redistribute                                    | - This command enables the redistribution of connected or static routes into the BGP routing table, allowing them to be advertised to BGP peers and become part of the BGP routing decision process<br>- value accepted for the argument `redistribute` are **connected** and **static** in a list. **Ex:** ["connected", "static"]<br>- command: **redistribute connected**<br>- command: **redistribute static** |

**&nbsp;&nbsp;&nbsp;&nbsp; Sample playbook task**

      - name: Sonic router BGP config
        sonic_bgp_address_family:
            config:
               - bgp_asn: 1001
                 address_family: # address-family
                   ipv4:  #address-family ipv4 unicast
                     neighbor:
                        ips: ['40.0.0.2','40.0.0.10']
                        allowas_in: 1   # 1-10 or origin
                     network: ['40.0.0.2/31','40.0.0.10/31']
                     redistribute: ["connected", "static"]

________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________

# MLAG
    Multi-Chassis Link Aggregation Group, executes the task with the module 
`sonic_mlag`. Provide the configuration data as a list under the “**config**” key. Here “**domain_id**” is the 
primary key.

**&nbsp;&nbsp;&nbsp;&nbsp; Supported keys/arguments - value:**

| key                 | description                                                                                                                                                                                                                                                                                                                                                                                                                    |
|---------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| domain_id           | - a primary key argument<br>- list of interface names. **Ex:** 1                                                                                                                                                                                                                                                                                                                                                               |
| peer_address        | - Sets the IP address of the peer MLAG switch to establish communication and synchronisation between MLAG-enabled switches<br>- provide the IP address. **Ex:** 10.4.4.4                                                                                                                                                                                                                                                       |
| src_address         | - Display LLDP neighbor information<br>- provide the IP address. **Ex:** 10.4.4.5                                                                                                                                                                                                                                                                                                                                              |
| peer_link           | - Provide a **port_channel id** or an **interface name**<br><br>- `port_channel`: Designates a port-channel as the communication link between MLAG switches, facilitating synchronization and control traffic. **Ex:** "portchannel20" / "pch10"<br><br>- `interface`: Assigns a physical Ethernet interface as the link for communication between MLAG switches, ensuring coordination and data exchange. **Ex:** "Ethernet4" |
| member_portchannels | - Configures a port-channel as a member of the MLAG for enhanced redundancy and load balancing<br>- Provide the list of port_channel<br>**Ex:** ["portchannel20", "pch10"]                                                                                                                                                                                                                                                     |
| local_interface     | - Provide a VLAN id. **Ex:** 100<br>- Configures a VLAN as the local interface for MLAG, allowing the MLAG-enabled switches to communicate and synchronize information for **enhanced redundancy** and **load balancing** within the specified VLAN                                                                                                                                                                            |

**&nbsp;&nbsp;&nbsp;&nbsp; Sample playbook task**

       - name: "Sonic Mlag creation "
         sonic_mlag:
            config:
               - domain_id: 1
                 peer_address: 192.168.0.3
                 peer_link: "portchannel999"
                 src_address: 192.168.0.2
                 member_portchannels: ['portchannel201','portchannel202', 'pch501']
                 local_interface: 10


________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________
