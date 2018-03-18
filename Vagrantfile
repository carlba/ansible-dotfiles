# -*- mode: ruby -*-
# vi: set ft=ruby :

module LocalCommand
    class Config < Vagrant.plugin("2", :config)
        attr_accessor :command
    end

    class Plugin < Vagrant.plugin("2")
        name "local_shell"

        config(:local_shell, :provisioner) do
            Config
        end

        provisioner(:local_shell) do
            Provisioner
        end
    end

    class Provisioner < Vagrant.plugin("2", :provisioner)
        def provision
            result = system "#{config.command}"
        end
    end
end

VAGRANT_NAME=File.basename(Dir.getwd)
CURRENT_DIRECTORY=Dir.pwd()
DEPLOY_ANSIBLE_GALAXY=true
ANSIBLE_REQUIREMENTS=if File.exist?('requirements.yml') then 'requirements.yml' else '../../requirements.yml' end
PLAYBOOK_NAME=if File.exist?('dotfiles.yml') then 'dotfiles.yml' else 'playbook.yml' end

# This Vagrantfile uses the multi-machine concept these links will be helpfull
# https://www.vagrantup.com/docs/multi-machine/
# https://manski.net/2016/09/vagrant-multi-machine-tutorial/

Vagrant.configure("2") do |config|
    # https://docs.vagrantup.com.

  config.vm.define "ubuntu_desktop" do |ubuntu_desktop|
    ubuntu_desktop.ssh.insert_key = false
    ubuntu_desktop.vm.box = "boxcutter/ubuntu_desktop1604-desktop"
    #config.vm.box = "mloskot/manjaro-i3-17.0-minimal"

    # Create a private network, which allows host-only access to the machine
    # using a specific IP.
    ubuntu_desktop.vm.network "private_network", type: "dhcp", nic_type: "virtio"

    # Create a public network, which generally matched to bridged network.
    # Bridged networks make the machine appear as another physical device on
    # your network.
    # config.vm.network "public_network"

    # Share an additional folder to the guest VM. The first argument is
    # the path on the host to the actual folder. The second argument is
    # the path on the guest to mount the folder. And the optional third
    # argument is a set of non-required options.
    # config.vm.synced_folder "../data", "/vagrant_data"

    # Provider-specific configuration so you can fine-tune various
    # backing providers for Vagrant. These expose provider-specific options.
    # Example for VirtualBox:
    #
    ubuntu_desktop.vm.provider "virtualbox" do |vb|
      # Display the VirtualBox GUI when booting the machine
      vb.gui = false

      # Customize the amount of memory on the VM:
      # vb.memory = "1024"

      # Set the name of the VirtualBox instance
      vb.name = VAGRANT_NAME + '_ubuntu_desktop'
    end
    ubuntu_desktop.vm.provision "ansible-galaxy", type: "local_shell" do |ansible_galaxy|
      ansible_galaxy.command = "ansible-galaxy install -r requirements.yml"
    end
    ubuntu_desktop.vm.provision "ansible" do |ansible|
      ansible.playbook = PLAYBOOK_NAME
      ansible.ask_vault_pass = true
      ansible.extra_vars = {"ansible_sudo_pass": "vagrant"}
    end
  end

  config.vm.define "manjaro" do |manjaro|
    manjaro.ssh.insert_key = false
    manjaro.vm.box = "mloskot/manjaro-i3-17.0-minimal"
    manjaro.vm.network "private_network", type: "dhcp", nic_type: "virtio"
    manjaro.vm.provider "virtualbox" do |vb|
      vb.gui = false
      #vb.memory = "1024"
      vb.name = VAGRANT_NAME + '_manjaro'
    end
    manjaro.vm.provision "ansible-galaxy", type: "local_shell" do |ansible_galaxy|
      ansible_galaxy.command = "ansible-galaxy install -r requirements.yml"
    end
    manjaro.vm.provision "ansible" do |ansible|
      ansible.playbook = PLAYBOOK_NAME
      ansible.ask_vault_pass = true
      ansible.extra_vars = {"ansible_sudo_pass": "vagrant"}
    end
  end

  config.vm.define "centos7" do |centos7|
    centos7.ssh.insert_key = false
    centos7.vm.box = "bento/centos-7.2"
    centos7.vm.network "private_network", type: "dhcp", nic_type: "virtio"
    centos7.vm.provider "virtualbox" do |vb|
      vb.gui = false
      #vb.memory = "1024"
      vb.name = VAGRANT_NAME + '_centos7'
    end
    centos7.vm.provision "ansible-galaxy", type: "local_shell" do |ansible_galaxy|
      ansible_galaxy.command = "ansible-galaxy install -r ansible/requirements.yml"
    end
    centos7.vm.provision "ansible" do |ansible|
      ansible.playbook = "common.yml"
      ansible.extra_vars = {"ansible_sudo_pass": "vagrant"}
    end
  end

  # https://app.vagrantup.com/ubuntu/boxes/artful64
  config.vm.define "ubuntu" do |ubuntu|
    ubuntu.ssh.insert_key = false
    ubuntu.vm.box = "ubuntu/artful64"
    ubuntu.vm.network "private_network", ip: "10.149.138.151", nic_type: "virtio"
    ubuntu.vm.provider "virtualbox" do |vb|
      vb.gui = false
      vb.name = VAGRANT_NAME + '_ubuntu'
    end
    ubuntu.vm.provision "ansible-galaxy", type: "local_shell" do |ansible_galaxy|
      ansible_galaxy.command = "ansible-galaxy install -r requirements.yml"
    end
    ubuntu.vm.provision "ansible" do |ansible|
      ansible.playbook = "server.yml"
      ansible.extra_vars = {"ansible_sudo_pass": "vagrant"}
    end
  end
end
