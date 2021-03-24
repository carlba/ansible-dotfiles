setup:
  rm -rf venv
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ansible-galaxy install -r requirements.yml

update:
  pip install -r requirements.txt
  ansible-galaxy install -r requirements.yml

create_vault_pass_file:
 touch ~/.vault_pass.txt; read -s -p "Enter Password: " password ; echo -n $password > ~/.vault_pass.txt
