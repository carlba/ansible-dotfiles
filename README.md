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
   virtualenv -p python2 venv; source venv/bin/activate
   pip install -r requirements.txt
   ansible-galaxy install -r requirements.yml --roles-path=tests/roles
   ```
   
# Usage
``` bash
ansible-galaxy install -r requirements.yml
ansible-playbook -i "localhost," --ask-vault-pass -K playbook.yml
```
