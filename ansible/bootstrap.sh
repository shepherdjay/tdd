#!/bin/bash

yum -y install epel-release
yum -y install ansible

echo "Running Ansible playbook, please be patient..."
ansible-playbook -i /ansible/inventory.ini -c local /ansible/playbook.yml
