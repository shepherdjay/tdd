# -*- mode: ruby -*-
# vi: set ft=ruby tabstop=2 shiftwidth=2 expandtab :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "dharmab/centos6"

  # Share the Ansible playbook for self-provisioning
  config.vm.synced_folder "ansible/", "/ansible/", owner: "root",
    group: "root", mount_options: ["dmode=755", "fmode=644"]

  # Script which bootstraps Ansible
  config.vm.provision "shell", path: "ansible/bootstrap.sh"
end
