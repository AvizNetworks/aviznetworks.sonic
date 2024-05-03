#!/bin/sh

# ~/.ansible/collections/ansible_collections/aviznetworks/sonic_fmcli


namespace=aviznetworks
name=ansible
version=1.0.0
collection_file="$namespace-$name-$version.tar.gz"
echo "$collection_file"

# rm -f /root/ansible_log.log
# ansible-galaxy collection install ansible.netcommon --force

if [ -n "$SUDO_USER" ]; then
    invoking_user=$SUDO_USER
else
    # If not set, fall back to the current user
    invoking_user=$USER
fi

echo $invoking_user

mkdir -p /home/$invoking_user/.ansible/collections/ansible_collections/aviznetworks/ansible
rm -rf /home/$invoking_user/.ansible/collections/ansible_collections/aviznetworks/ansible/* 
sudo cp -rfu ./../aviznetworks.sonic/* /home/$invoking_user/.ansible/collections/ansible_collections/aviznetworks/ansible/
echo "ls to /home/$invoking_user/.ansible/collections/ansible_collections/aviznetworks/ansible/"
ls /home/$invoking_user/.ansible/collections/ansible_collections/aviznetworks/ansible/


mkdir -p /root/.ansible/collections/ansible_collections/aviznetworks/ansible
rm -rf /root/.ansible/collections/ansible_collections/aviznetworks/ansible/*
cp -rfu ./../aviznetworks.sonic/* /root/.ansible/collections/ansible_collections/aviznetworks/ansible/
echo "ls to /root/.ansible/collections/ansible_collections/aviznetworks/ansible/"
ls /root/.ansible/collections/ansible_collections/aviznetworks/ansible/


# sudo rm -rf /root/.ansible/collections/ansible_collections/aviznetworks/sonic_fmcli/*

# sudo cp -r ./../aviznetworks.sonic_fmcli/* /root/.ansible/collections/ansible_collections/aviznetworks/sonic_fmcli/

# sudo rm -rf ~/.ansible/collections/ansible_collections/aviznetworks/sonic_fmcli/*

# sudo cp -r -f ./../aviznetworks.sonic_fmcli/* ~/.ansible/collections/ansible_collections/aviznetworks/sonic_fmcli/


# file_path="$HOME/.ssh/config"
# host_key_checking="StrictHostKeyChecking=accept-new"
# touch $file_path
# if ! grep -q "$host_key_checking" "$file_path"; then
#     echo "$host_key_checking" | tee -a "$file_path" > /dev/null


# execute this file from current location and with sudo permission
# sudo sh ./rebuild.sh