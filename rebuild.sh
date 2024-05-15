#!/bin/sh

# ~/.ansible/collections/ansible_collections/aviznetworks/sonic


namespace=aviznetworks
name=ansible
version=1.0.0
collection_file="$namespace-$name-$version.tar.gz"
echo "$collection_file"

rm -f /root/ansible_log.log
ansible-galaxy collection install ansible.netcommon --force

if [ -n "$SUDO_USER" ]; then
    invoking_user=$SUDO_USER
else
    # If not set, fall back to the current user
    invoking_user=$USER
fi

echo $invoking_user

mkdir -p /home/$invoking_user/.ansible/collections/ansible_collections/aviznetworks/sonic
rm -rf /home/$invoking_user/.ansible/collections/ansible_collections/aviznetworks/sonic/*
sudo cp -rfu ./../aviznetworks.sonic/* /home/$invoking_user/.ansible/collections/ansible_collections/aviznetworks/sonic/
echo "ls to /home/$invoking_user/.ansible/collections/ansible_collections/aviznetworks/sonic/"
ls /home/$invoking_user/.ansible/collections/ansible_collections/aviznetworks/sonic/


mkdir -p /root/.ansible/collections/ansible_collections/aviznetworks/sonic
rm -rf /root/.ansible/collections/ansible_collections/aviznetworks/sonic/*
cp -rfu ./../aviznetworks.sonic/* /root/.ansible/collections/ansible_collections/aviznetworks/sonic/
echo "ls to /root/.ansible/collections/ansible_collections/aviznetworks/sonic/"
ls /root/.ansible/collections/ansible_collections/aviznetworks/sonic/

