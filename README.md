# ansible-dotfiles

# Cloning
This project contains submodules so use when cloning. So make sure the repo is cloned recursively, like so:

``` bash
git clone --recursive https://github.com/carlba/ansible-dotfiles
```

# Usage

``` bash
ansible-galaxy install -r requirements.yml
ansible-playbook -i "localhost," --ask-vault-pass -K playbook.yml
```
