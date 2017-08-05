# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANT_NAME=File.basename(Dir.getwd)
CURRENT_DIRECTORY=Dir.pwd()
DEPLOY_ANSIBLE_GALAXY=true
ANSIBLE_REQUIREMENTS=if File.exist?('requirements.yml') then 'requirements.yml' else '../../requirements.yml' end
PLAYBOOK_NAME=if File.exist?('dotfiles.yml') then 'dotfiles.yml' else 'playbook.yml' end

# This Vagrantfile uses the multi-machine concept these links will be helpfull
# https://www.vagrantup.com/docs/multi-machine/
# https://manski.net/2016/09/vagrant-multi-machine-tutorial/

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.

Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  config.vm.define "ubuntu" do |ubuntu|
    ubuntu.ssh.insert_key = true
    # Every Vagrant development environment requires a box. You can search for
    # boxes at https://app.vagrantup.com/boxes/search.

    ubuntu.vm.box = "boxcutter/ubuntu1604-desktop"
    #config.vm.box = "mloskot/manjaro-i3-17.0-minimal"
    #config.vm.box = "bento/centos-7.2"

    # Disable automatic box update checking. If you disable this, then
    # boxes will only be checked for updates when the user runs
    # `vagrant box outdated`. This is not recommended.
    # config.vm.box_check_update = false

    # Create a forwarded port mapping which allows access to a specific port
    # within the machine from a port on the host machine. In the example below,
    # accessing "localhost:8080" will access port 80 on the guest machine.
    # config.vm.network "forwarded_port", guest: 80, host: 8080

    # Create a private network, which allows host-only access to the machine
    # using a specific IP.
    ubuntu.vm.network "private_network", type: "dhcp", nic_type: "virtio"

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
    ubuntu.vm.provider "virtualbox" do |vb|
      # Display the VirtualBox GUI when booting the machine
      vb.gui = false

      # Customize the amount of memory on the VM:
      # vb.memory = "1024"

      # Set the name of the VirtualBox instance
      vb.name = VAGRANT_NAME + '_ubuntu'
    end

    # View the documentation for the provider you are using for more
    # information on available options.

    # Define a Vagrant Push strategy for pushing to Atlas. Other push strategies
    # such as FTP and Heroku are also available. See the documentation at
    # https://docs.vagrantup.com/v2/push/atlas.html for more information.
    # config.push.define "atlas" do |push|
    #   push.app = "YOUR_ATLAS_USERNAME/YOUR_APPLICATION_NAME"
    # end

    # Enable provisioning with a shell script. Additional provisioners such as
    # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
    # documentation for more information about their specific syntax and use.
    # config.vm.provision "shell", inline: <<-SHELL
    #   apt-get update
    #   apt-get install -y apache2
    # SHELL

    # https://www.vagrantup.com/docs/provisioning/ansible_intro.html
    # https://www.vagrantup.com/docs/provisioning/ansible.html
    ubuntu.vm.provision "ansible" do |ansible|
      ansible.playbook = PLAYBOOK_NAME
      ansible.galaxy_role_file=ANSIBLE_REQUIREMENTS if DEPLOY_ANSIBLE_GALAXY
      ansible.ask_vault_pass = true
      ansible.extra_vars = {"ansible_sudo_pass": "vagrant"}
    end
  end

  config.vm.define "manjaro" do |manjaro|
    manjaro.ssh.insert_key = true
    manjaro.vm.box = "mloskot/manjaro-i3-17.0-minimal"
    manjaro.vm.network "private_network", type: "dhcp", nic_type: "virtio"

    manjaro.vm.provider "virtualbox" do |vb|
      vb.gui = false
      #vb.memory = "1024"
      vb.name = VAGRANT_NAME + '_manjaro'
    end

    manjaro.vm.provision "ansible" do |ansible|
      ansible.playbook = PLAYBOOK_NAME
      ansible.galaxy_role_file=ANSIBLE_REQUIREMENTS if DEPLOY_ANSIBLE_GALAXY
      ansible.ask_vault_pass = true
      ansible.extra_vars = {"ansible_sudo_pass": "vagrant"}
    end
  end


  config.vm.define "centos7" do |centos7|
    centos7.ssh.insert_key = true
    centos7.vm.box = "bento/centos-7.2"
    centos7.vm.network "private_network", type: "dhcp", nic_type: "virtio"

    centos7.vm.provider "virtualbox" do |vb|
      vb.gui = false
      #vb.memory = "1024"
      vb.name = VAGRANT_NAME + '_centos7'
    end

    centos7.vm.provision "ansible" do |ansible|
      ansible.playbook = "common.yml"
      ansible.galaxy_role_file=ANSIBLE_REQUIREMENTS if DEPLOY_ANSIBLE_GALAXY
      ansible.extra_vars = {"ansible_sudo_pass": "vagrant"}
    end
  end
end
