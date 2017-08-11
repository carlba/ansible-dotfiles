
from __future__ import print_function


import os
import sys
import shutil

import click
from sh import ansible_playbook
import pygit2

HOME_PATH = os.path.expanduser("~")

ansible_dotfiles_path = None

def process_output(line):
    print(line, end='')

@click.group()
def cli():
    pass

@click.command()
def list():
    for item in os.listdir('roles'):
        print(item)

@click.command()
@click.argument('role', nargs=1)
def play(role):
    if role not in os.listdir('roles'):
        raise click.BadParameter('The role does not exist')

    sudo_password = click.prompt('SUDO Password', type=str, hide_input=True)


    ansible_playbook(
        '-c', 'local' ,'-i', 'localhost,', '-e', 'ansible_sudo_pass={}'.format(sudo_password),
        '--vault-password-file', os.path.join(HOME_PATH, '.vault_pass.txt'),
        os.path.join(ansible_dotfiles_path,'roles', role, 'playbook.yml'), _out=process_output)

cli.add_command(list)
cli.add_command(play)

if __name__ == '__main__':
    in_dotfiles_repo = os.path.isfile('dotfiles.yml') and os.path.isdir('roles')
    if not in_dotfiles_repo:
        if os.path.isdir('/tmp/ansible-dotfiles'):
            shutil.rmtree('/tmp/ansible-dotfiles')

        repo = pygit2.clone_repository('https://github.com/carlba/ansible-dotfiles.git',
            '/tmp/ansible-dotfiles')

        ansible_dotfiles_path = repo.path
    else:
        ansible_dotfiles_path = os.getcwd()

    cli()
