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
ansible==2.10.6
ansible-base==2.10.5
appdirs==1.4.4
asn1crypto==1.4.0
bcrypt==3.2.0
cffi==1.14.4
click==7.1.2
cryptography==3.2
distlib==0.3.1
enum34==1.1.10
filelock==3.0.12
idna==2.10
ipaddress==1.0.23
Jinja2==2.11.2
MarkupSafe==1.1.1
packaging==20.9
paramiko==2.7.1
pyasn1==0.4.8
pycparser==2.20
PyNaCl==1.4.0
pyparsing==2.4.7
PyYAML==5.3.1
sh==1.13.1
six==1.15.0
EOF

pip3 install -q -r requirements.txt
