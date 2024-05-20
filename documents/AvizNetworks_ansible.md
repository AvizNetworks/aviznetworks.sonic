***********Ansible Module aviznetworks.sonic***********
=======================================================


________________________________________________________
________________________________________________________


# Day-2...day-n configuration difference

In the Ansible script tasks, the `aviznetworks.sonic` module will check and compare the configuration of each task with the existing configuration on the devices. The module will merge the configurations if a similar configuration supports the protocol rules, or the new configurations will override it.

### Example:

**Day-1 Configuration**

    - name: SONiC port configuration
        sonic_interfaces:
            config:
                - interface: ["Ethernet32", "Ethernet4"]
                  mtu: 9000
                  enable: True

**Day-2 Configuration**
    
    - name: SONiC port configuration
        sonic_interfaces:
            config:
                - interface: ["Ethernet32"]
                  mtu: 9100
                  enable: True
                  description: "fmcli description_eth32"
    

In the example above, on `day-2 ... days-n` configuration, updating the MTU and configure the port description. In the log, `Diff` shows, removing the old mtu value and adding the new value. 
Only **description** getting added, because in the old configuration description was not provided.

### log:

    "diff": {
                "interfaces": {
                    "interface ethernet Ethernet32": [
                        "- mtu 9000",
                        "+ mtu 9100",
                        "+ description fmcli description_eth32",
                    ]
                }
            }

________________________________________________________
________________________________________________________

# State: Merge / Delete

Two State supports will `merge/delete` the configuration on `day-0 ... day-n` task operation.

## **1. Merge**
A default operation, will be used in case of `merge/add/update/override` configurations.

    # day-0

    - name: SONiC port configuration
         sonic_interfaces:
           config:
             - interface: ["Ethernet32"]
               mtu: 9000
               enable: True
               description: "fmcli description_eth32"
        
             - interface: ["Ethernet34"]
               mtu: 9000
               description: "fmcli description_eth34"
    
    
       state: merge  # default
    
    ____________________________________________________________________________________________________________________
    
    # day-n  
    
    - name: SONiC port configuration
         sonic_interfaces:
           config:
             - interface: ["Ethernet32"]
               mtu: 9000
               ip_address: 40.0.0.10/31 # new configuration
               description: "fmcli description_eth32"
           state: merge  # default


In this configuration, it will check if any configuration exists it will get overridden and if it does not exist it will get added as a new configuration.

### log:
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

## **2. Delete**

It will delete the configuration if it already exists.
    
   ### ***a) Delete inner configs***
    # day-0

    - name: SONiC port configuration
         sonic_interfaces:
           config:
             - interface: ["Ethernet32", "Ethernet36"]
               mtu: 9000
               enable: True
               description: "fmcli description"
           state: merge  # default

    ____________________________________________________________________________________________________________________

    # day-n delete some config. Ex: delete the description for the interfaces

    - name: SONiC port configuration
         sonic_interfaces:
           config:
             - interface: ["Ethernet32", "Ethernet36"]
               description: "fmcli description"
           state: delete

Here, `day-n` task will delete the inner configuration only mentioned under the interface.

### log:
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


   ### ***b) Delete whole configs***
    # day-0, day-1, ...

    - name: SONiC port configuration
        sonic_interfaces:
           config:
             - interface: ["Ethernet32", "Ethernet36"]
               mtu: 9000
               enable: True
               description: "fmcli description"


    ____________________________________________________________________________________________________________________
    # day-n delete whole config 

    - name: SONiC port configuration
        sonic_interfaces:
            config:
              - interface: ["Ethernet32", "Ethernet36"]
            state: delete  

Here, `day-n` task will delete the complete configuration for the listed interfaces

### log:
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

________________________________________________________
________________________________________________________

# Ports/Interface
Configuring and deleting multiple interfaces.
Executes the task with the module `sonic_interfaces`. Provide the configuration data as a list under the “**config**” key. Here “**interface**” is the primary key.

**Supported keys/arguments - value:**

| key         | description                                                                                                                                                                         |
|-------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| interface   | - a primary key argument<br/>- list of interface names. **Ex:** ["Ethernet32", "Ethernet4"]                                                                                         |
| mtu         | - mtu value, int type. **Ex:** 9100                                                                                                                                                 |
| enable      | - To enable or disable the ports, boolean type. **Ex:** true/false <br/> **true**: enable/bring-up the ports <br/> **false**: disable/bring-down the ports                          |
| ip_address  | - Configure the IP(v4) address to a port. <br/> - provide the IP address with a mask. **Ex:** 10.4.4.4/24 <br/> - make sure, use a single interface name for the argument interface |
| description | Description of interfaces                                                                                                                                                           |
| fec         | - forward-error-correction <br/> - Choose a value from the list: `["rs", "fc", "none"]`                                                                                             |
| speed       | - Choose a value from the list:`["1G", "10G", "25G", "40G", "50G", "100G", "400G"]`                                                                                                 |

Sample playbook task

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


________________________________________________________
________________________________________________________
