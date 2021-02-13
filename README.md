ansible-dotfiles
================

Deploys my minimal personalized dotfiles suitable for CLI usage.

Setup the environment
---------------------

1. Clone the repository recursively
   ```bash
   git clone --recursive https://github.com/carlba/ansible-dotfiles
   ```

2. Install the ansible environment
   ```bash
   python3 -m venv venv; source venv/bin/activate
   pip install -r requirements.txt
   ansible-galaxy install -r requirements.yml
   ```
3. Create an ansible password vault file  
   ```bash
   touch ~/.vault_pass.txt; read -s -p "Enter Password: " password ; echo -n $password > ~/.vault_pass.txt
   ``` 
   
Usage
-----

``` bash
ansible-galaxy install -r requirements.yml
ansible-playbook -i "localhost," --diff  dotfiles.yml
```

### MacOS

* The Karabiner Element complex modification must be manually activated in 
  Harbinger Elements/Complex Modifications/Add Rule. After the playbook is executed there 
  will be a rule called `Change caps_lock to command+space`.

* Due to Ansible not being possible to run on the Mac M1 it currently is running under
  Rosetta emulation. This causes the `homebrew_cask` ansible plugin to install apps
  for X86 rather then the ones optimized for ARM. The Homebrew related tasks should
  be executed using this command instead.
  
  ```bash
  brew reinstall --cask plex
  brew reinstall --cask alfred
  brew reinstall --cask macpass
  brew reinstall --cask transmission-remote-gui
  brew reinstall --cask resolutionator
  brew reinstall --cask typora
  brew reinstall --cask iterm2
  brew reinstall --cask google-backup-and-sync
  brew reinstall --cask Karabiner-Elements
  brew reinstall --cask pigz
  ```