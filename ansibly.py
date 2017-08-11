
from __future__ import print_function


import os

# noinspection PyUnresolvedReferences
from sh import (ansible_playbook, ansible_galaxy, git, wget, tar, cd, cmake, make, pip, ldconfig)
# noinspection PyUnresolvedReferences
from sh.contrib import sudo
# import pygit2
import temporary
import click


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
        pip('install', 'pygit2', _out=process_output)





