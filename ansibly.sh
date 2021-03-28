#!/bin/bash

dist=$(lsb_release -ds 2>/dev/null || cat /etc/*release 2>/dev/null | head -n1 || uname -om)


if [[ $dist == *"CentOS"* ]]; then
  sudo yum install -y git gcc python-devel > /dev/null
fi

if [[ $dist == *"Manjaro"* ]]; then
  sudo pacman --noconfirm -S git gcc > /dev/null
fi

curl --silent https://bootstrap.pypa.io/get-pip.py | sudo python2 > /dev/null

tee requirements.txt <<EOF > /dev/null
ansible==2.3.2.0
asn1crypto==0.22.0
bcrypt==3.1.3
cffi==1.10.0
click==6.7
cryptography==2.0.3
enum34==1.1.6
idna==2.6
ipaddress==1.0.18
Jinja2==2.9.6
MarkupSafe==1.0
paramiko==2.2.1
pyasn1==0.3.2
pycparser==2.18
pycrypto==2.6.1
PyNaCl==1.1.2
PyYAML==3.12
sh==1.12.14
six==1.10.0
virtualenv
EOF

pip3 install -q -r requirements.txt
