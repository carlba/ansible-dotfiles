#!/bin/bash
cd ../
mkdir -p library/external_modules
git submodule add git://github.com/cdown/ansible-aur.git library/external_modules/ansible-aur
ln -s external_modules/ansible-aur/aur library/aur