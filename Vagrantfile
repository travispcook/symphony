# -*- mode: ruby -*-
# # vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "coreos"
  config.vm.box_url = "http://storage.core-os.net/coreos/amd64-generic/dev-channel/coreos_production_vagrant.box"

  # Fix docker not being able to resolve private registry in VirtualBox
  config.vm.provider :virtualbox do |vb, override|
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
    config.vm.network "private_network", ip: "192.168.200.2"
    config.vm.synced_folder ".", "/home/core/symphony", id: "core", :nfs => true,  :mount_options   => ['nolock,vers=3,udp']
  end
end
