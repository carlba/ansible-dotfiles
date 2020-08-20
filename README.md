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
  Karabiner Elements/Complex Modifications/Add Rule. After the playbook is executed there 
  will be a rule called `Change caps_lock to command+space`.
