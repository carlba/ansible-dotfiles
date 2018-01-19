# ansible-dotfiles

# Cloning
This project contains submodules which means it is instrumental to clone the repository recursivly like so:

``` bash
git clone --recursive https://github.com/carlba/ansible-dotfiles
```

# Usage

``` bash
ansible-galaxy install -r requirements.yml
ansible-playbook -i "localhost," --ask-vault-pass -K playbook.yml
```
