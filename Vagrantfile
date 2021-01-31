# -*- mode: ruby -*-
# vi: set ft=ruby :

module LocalCommand
    class Config < Vagrant.plugin('2', :config)
        attr_accessor :command
    end

    class Plugin < Vagrant.plugin('2')
        name 'local_shell'

        config(:local_shell, :provisioner) do
            Config
        end

        provisioner(:local_shell) do
            Provisioner
        end
    end

    class Provisioner < Vagrant.plugin('2', :provisioner)
        def provision
            result = system '#{config.command}'
        end
    end
end

VAGRANT_NAME ||= File.basename(Dir.getwd)
CURRENT_DIRECTORY ||= Dir.pwd()
DEPLOY_ANSIBLE_GALAXY ||= false
ANSIBLE_REQUIREMENTS ||= if File.exist?('requirements.yml') then 'requirements.yml' else '../../requirements.yml' end
PLAYBOOK_NAME ||= if File.exist?('tests/test.yml') then 'tests/test.yml' elsif File.exist?('dotfiles.yml') then 'dotfiles.yml' else 'playbook.yml' end

# This Vagrantfile uses the multi-machine concept these links will be helpful
# https://www.vagrantup.com/docs/multi-machine/
# https://manski.net/2016/09/vagrant-multi-machine-tutorial/
# https://docs.vagrantup.com
Vagrant.configure('2') do |config|
  config.vm.define 'ubuntu_desktop' do |ubuntu_desktop|
    ubuntu_desktop.ssh.insert_key = false
    ubuntu_desktop.vm.box = 'peru/ubuntu-18.04-desktop-amd64'
    ubuntu_desktop.vm.network 'private_network', type: 'dhcp', nic_type: 'virtio'
    # config.vm.network 'public_network'
    # config.vm.synced_folder '../data', '/vagrant_data'

    ubuntu_desktop.vm.provider 'virtualbox' do |vb|
      vb.gui = false
      vb.name = VAGRANT_NAME + '_ubuntu_desktop'
    end

    ubuntu_desktop.vm.provision 'ansible-galaxy', type: 'local_shell' do |ansible_galaxy|
      ansible_galaxy.command = 'ansible-galaxy install -r requirements.yml --roles-path=roles'
    end

    ubuntu_desktop.vm.provision 'ansible' do |ansible|
      ansible.playbook = PLAYBOOK_NAME
      ansible.extra_vars = {'ansible_sudo_pass': 'vagrant',
                            'is_privileged_user': true,
                            'ansible_python_interpreter': 'python3'}
      ansible.config_file = 'ansible.cfg'
      ansible.raw_arguments = ['--diff']
      ansible.groups = {'vagrant' => ['ubuntu_desktop']}
    end
  end

  config.vm.define 'manjaro' do |manjaro|
    manjaro.ssh.insert_key = false
    manjaro.vm.box = 'mloskot/manjaro-i3-17.0-minimal'
    manjaro.vm.network 'private_network', type: 'dhcp', nic_type: 'virtio'

    manjaro.vm.provider 'virtualbox' do |vb|
      vb.gui = false
      vb.name = VAGRANT_NAME + '_manjaro'
    end

    manjaro.vm.provision 'ansible-galaxy', type: 'local_shell' do |ansible_galaxy|
      ansible_galaxy.command = 'ansible-galaxy install -r requirements.yml --roles-path=roles'
    end

    manjaro.vm.provision 'ansible' do |ansible|
      ansible.playbook = PLAYBOOK_NAME
      ansible.extra_vars = {'ansible_sudo_pass': 'vagrant',
                            'is_privileged_user': true}
      ansible.config_file = 'ansible.cfg'
      ansible.raw_arguments = ['--diff']
      ansible.groups = {'vagrant' => ['manjaro']}
    end
  end

  config.vm.define 'centos7' do |centos7|
    centos7.ssh.insert_key = false
    centos7.vm.box = 'bento/centos-7.4'
    centos7.vm.network 'private_network', type: 'dhcp', nic_type: 'virtio'

    centos7.vm.provider 'virtualbox' do |vb|
      vb.gui = false
      vb.name = VAGRANT_NAME + '_centos7'
    end

    centos7.vm.provision 'ansible-galaxy', type: 'local_shell' do |ansible_galaxy|
      ansible_galaxy.command = 'ansible-galaxy install -r requirements.yml --roles-path=roles'
    end

    centos7.vm.provision 'ansible' do |ansible|
      ansible.playbook = 'dotfiles_minimal.yml'
      ansible.extra_vars = {'ansible_sudo_pass': 'vagrant',
                            'is_privileged_user': true}
      ansible.config_file = 'ansible.cfg'
      ansible.raw_arguments = ['--diff']
      ansible.groups = {'vagrant' => ['centos7']}
    end
  end

  # https://app.vagrantup.com/ubuntu/boxes/artful64
  config.vm.define 'ubuntu' do |ubuntu|
    ubuntu.ssh.insert_key = false
    ubuntu.vm.box = 'ubuntu/artful64'
    ubuntu.vm.network 'private_network', type: 'dhcp', nic_type: 'virtio'

    ubuntu.vm.provider 'virtualbox' do |vb|
      # vb.gui = false
      vb.name = VAGRANT_NAME + '_ubuntu'
    end

    ubuntu.vm.provision 'ansible-galaxy', type: 'local_shell' do |ansible_galaxy|
      ansible_galaxy.command = 'ansible-galaxy install -r requirements.yml --roles-path=roles'
    end

    ubuntu.vm.provision 'ansible' do |ansible|
      ansible.playbook = 'dotfiles_minimal.yml'
      ansible.extra_vars = {'ansible_sudo_pass': 'vagrant',
                            'is_privileged_user': true,
                            'ansible_python_interpreter': 'python3'}
      ansible.config_file = 'ansible.cfg'
      ansible.raw_arguments = ['--diff']
      ansible.groups = {'vagrant' => ['ubuntu']}
    end
  end

  # # https://app.vagrantup.com/andreiborisov/boxes/macos-bigsur-intel
  # config.vm.define 'macos' do |macos|
  #   macos.ssh.insert_key = false
  #   macos.vm.box = 'andreiborisov/macos-bigsur-intel'
  #   macos.vm.network 'private_network', type: 'dhcp', nic_type: 'virtio'

  #   macos.vm.provider 'virtualbox' do |vb|
  #     # vb.gui = false
  #     vb.name = VAGRANT_NAME + '_macos'
  #   end

  #   macos.vm.provision 'ansible-galaxy', type: 'local_shell' do |ansible_galaxy|
  #     ansible_galaxy.command = 'ansible-galaxy install -r requirements.yml --roles-path=roles'
  #   end

  #   macos.vm.provision 'ansible' do |ansible|
  #     ansible.playbook = PLAYBOOK_NAME
  #     ansible.extra_vars = {'ansible_sudo_pass': 'vagrant',
  #                           'is_privileged_user': true,
  #                           'ansible_python_interpreter': 'python3'}
  #     ansible.config_file = 'ansible.cfg'
  #     ansible.raw_arguments = ['--diff']
  #     ansible.groups = {'vagrant' => ['ubuntu']}
  #   end
  # end

end
