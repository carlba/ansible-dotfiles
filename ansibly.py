
from __future__ import print_function


import os

import pip

requirements = [
    ['cffi', '1.10.0'],
    ['click', '6.7'],
    ['contextlib2', '0.5.5'],
    ['pathlib2', '2.3.0'],
    ['pycparser', '2.18'],
    ['pygit2', '0.26.0'],
    ['scandir', '1.5'],
    ['sh', '1.12.14'],
    ['six', '1.10.0'],
    ['temporary', '3.0.0']
]

def ensure_python_dependency(name, version):
    installed_packages = pip.get_installed_distributions()
    for item in installed_packages:
        if item.project_name == name:
            break
    else:
        pip.main(["install", "{}=={}".format(name, version)])

for requirement in requirements:
        ensure_python_dependency(requirement[0], requirement[1])

import temporary
import click


# noinspection PyUnresolvedReferences
from sh import (ansible_playbook, ansible_galaxy, git, wget, tar, cd, cmake, make,
                pip as pip_command, ldconfig)
# noinspection PyUnresolvedReferences
from sh.contrib import sudo

HOME_PATH = os.path.expanduser("~")
TEMP_PATH = '/tmp/ansible-dotfiles'


def process_output(line):
    """
    Callback for printing output from sh commands
    :param line:
    """
    print(line, end='')


def install_libgit2():
    # https://pypi.python.org/pypi/temporary
    with temporary.temp_dir(make_cwd=True) as temp_dir:
        wget('https://github.com/libgit2/libgit2/archive/v0.26.0.tar.gz', _out=process_output)
        # noinspection SpellCheckingInspection
        tar('-xzvf', 'v0.26.0.tar.gz', _out=process_output)
        os.chdir(os.path.join(os.getcwd(), 'libgit2-0.26.0'))
        cmake('.', _out=process_output)
        make(_out=process_output)
        with sudo:
            make.install(_out=process_output)

@click.group()
@click.pass_context
def cli(ctx):
    in_dotfiles_repo = os.path.isfile('dotfiles.yml') and os.path.isdir('roles')
    if not in_dotfiles_repo:
        if os.path.isdir(TEMP_PATH):
            repo = pygit2.Repository(TEMP_PATH)
            repo.remotes['origin'].fetch()
            repo.checkout('HEAD', strategy=pygit2.GIT_CHECKOUT_FORCE)
        else:
            repo = pygit2.clone_repository('https://github.com/carlba/ansible-dotfiles.git',
                                           TEMP_PATH)
        ansible_dotfiles_path = os.path.dirname(repo.path.rstrip('/'))
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

    try:
        import pygit2
    except ImportError as error:
        install_libgit2()
        with sudo:
            ldconfig()
        pip.main(['install', 'pygit2'])
    cli(obj={})





