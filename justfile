python_venv_bin := "venv/bin"
set dotenv-load := true

_header name:
  @echo '{{ name }}'

install:
  #!/usr/bin/env bash
  echo "Removing old venv if it exists"
  rm -rf venv
  echo "Create new venv"
  python3 -m venv venv
  echo "Source venv"
  source venv/bin/activate
  echo "Ensure python requirements from requirements.txt is installed"
  pip install -r requirements.txt
  echo "Ensure Ansible Galaxy requirements from requirements.yml"
  ansible-galaxy install -r requirements.yml

update:
  #!/usr/bin/env bash
  echo "Source venv"
  source venv/bin/activate
  echo "Ensure python requirements from requirements.txt is installed"
  pip install -r requirements.txt
  echo "Ensure Ansible Galaxy requirements from requirements.yml"
  ansible-galaxy install --force -r requirements.yml

format:
  @echo "Formatting all files using prettier"
  @prettier --write .

create_vault_pass_file:
  touch ~/.vault_pass.txt; read -s -p "Enter Password: " password ; echo -n $password > ~/.vault_pass.txt

