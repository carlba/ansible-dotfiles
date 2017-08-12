
from __future__ import print_function


import os
import imp
import virtualenv

venv_dir = "/tmp/.venv"
virtualenv.create_environment(venv_dir)
activate_script = os.path.join(venv_dir, "bin", "activate_this.py")
execfile(activate_script, dict(__file__=activate_script))

import pip

requirements = [
    ['cffi', '1.10.0'],
    ['click', '6.7'],
    ['contextlib2', '0.5.5'],
    ['pathlib2', '2.3.0'],
    ['pycparser', '2.18'],
    ['scandir', '1.5'],
    ['sh', '1.12.14'],
    ['six', '1.10.0'],
    ['temporary', '3.0.0']
]

def ensure_python_dependency(name, version, path=None):
    try:
        if path:
            imp.find_module(name, path)
        else:
            imp.find_module(name)
    except ImportError as e:
        pass
    else:
        pip.main(["install", "{}=={}".format(name, version), "--prefix", venv_dir])

for requirement in requirements:
        ensure_python_dependency(requirement[0], requirement[1], venv_dir)

import temporary
import click
import sh

# noinspection PyUnresolvedReferences
from sh import (ansible_playbook, ansible_galaxy, git, wget, tar, cd)

HOME_PATH = os.path.expanduser("~")
TEMP_PATH = '/tmp/ansible-dotfiles'


def process_output(line):
    """
    Callback for printing output from sh commands
    :param line:
    """
    print(line, end='')

@click.group()
@click.pass_context
def cli(ctx):
    in_dotfiles_repo = os.path.isfile('dotfiles.yml') and os.path.isdir('roles')
    if not in_dotfiles_repo:
        if os.path.isdir(TEMP_PATH):
            os.chdir(TEMP_PATH)
            git.fetch('--all')
            git.reset('--hard', 'HEAD')
        else:
            git('-C', '/tmp/ansible-dotfiles').clone('https://github.com/carlba/ansible-dotfiles.git')

        ansible_dotfiles_path = TEMP_PATH
    else:
        ansible_dotfiles_path = os.getcwd()

    ctx.obj['ansible_dotfiles_path'] = ansible_dotfiles_path


@click.command()
@click.pass_context
def list(ctx):
    """
    List all roles available in the Ansible repo

    :param ctx: The click command context
    """
    for item in os.listdir(os.path.join(ctx.obj['ansible_dotfiles_path'], 'roles')):
        print(item)


@click.command()
@click.pass_context
@click.argument('role', nargs=1)
def play(ctx, role):
    if role not in os.listdir(os.path.join(ctx.obj['ansible_dotfiles_path'],'roles')):
        raise click.BadParameter('The role does not exist')

    vault_pass_file_path = os.path.join(HOME_PATH, '.vault_pass.txt')

    if not os.path.isfile(vault_pass_file_path):
        raise click.FileError(vault_pass_file_path, hint='A file containing the Vault '
                                                         'password is required')

    new_env = os.environ.copy()
    new_env['ANSIBLE_ROLES_PATH'] = os.path.join(ctx.obj['ansible_dotfiles_path'],'roles')

    sudo_password = click.prompt('SUDO Password', type=str, hide_input=True)

    ansible_galaxy('--roles-path', new_env['ANSIBLE_ROLES_PATH'],
                   '--role-file', os.path.join(ctx.obj['ansible_dotfiles_path'],
                                               'requirements.yml'),
                   'install', _out=process_output)

    ansible_playbook(
        '-c', 'local' ,'-i', 'localhost,', '-e', 'ansible_sudo_pass={}'.format(sudo_password),
        '--vault-password-file', os.path.join(HOME_PATH, '.vault_pass.txt'),
        os.path.join(ctx.obj['ansible_dotfiles_path'],'roles', role, 'playbook.yml'),
        _out=process_output, _env=new_env)

cli.add_command(list)
cli.add_command(play)

if __name__ == '__main__':


    cli(obj={})





