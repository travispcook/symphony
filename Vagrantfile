# -*- mode: ruby -*-
# # vi: set ft=ruby :
$script = <<SCRIPT
apt-get -q update && apt-get -qy dist-upgrade
wget -O- https://get.docker.io/ubuntu/ | sh
apt-get -qy install python-pip
pip install docker-py
SCRIPT

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu_12.04_raring_kernel"
  config.vm.box_url = "http://nitron-vagrant.s3-website-us-east-1.amazonaws.com/vagrant_ubuntu_12.04.3_amd64_virtualbox.box"
  config.vm.provider :virtualbox do |vb, override|
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
    config.vm.network "private_network", ip: "192.168.200.2"
    config.vm.synced_folder ".", "/home/vagrant/symphony", id: "core", :nfs => true,  :mount_options   => ['nolock,vers=3,udp']
  end

  config.vm.provider "vmware_fusion" do |v, override|
    override.vm.box_url = "http://nitron-vagrant.s3-website-us-east-1.amazonaws.com/vagrant_ubuntu_12.04.3_amd64_vmware.box"
  end

  config.vm.provision "shell", inline: $script

  config.vm.provision "docker" do |d|
    d.run "symphony",
        image: "cellofellow/symphony",
        args: "-v '/home/vagrant/symphony:/opt/symphony' -name symphony"
  end
end
