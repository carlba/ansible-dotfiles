
from __future__ import print_function


import os
import click

# noinspection PyUnresolvedReferences
from sh import (ansible_playbook, ansible_galaxy, git, ErrorReturnCode_2)

HOME_PATH = os.path.expanduser("~")
TEMP_PATH = '/tmp/ansible-dotfiles'
REPO_PATH = os.path.expanduser("~/development/ansible-dotfiles")


def _process_output(line):
    """
    Callback for printing output from sh commands
    :param line:
    """
    print(line, end='')


@click.group()
@click.pass_context
def cli(ctx):
    if ctx.obj is None:
        ctx.obj = {}

    in_dotfiles_repo = os.path.isfile('dotfiles.yml') and os.path.isdir('roles')
    dotfiles_repo_exist = (os.path.isfile(os.path.join(REPO_PATH, 'dotfiles.yml')) and
                           os.path.isdir(os.path.join(REPO_PATH, 'roles')))

    if in_dotfiles_repo:
        ansible_dotfiles_path = os.getcwd()
    elif dotfiles_repo_exist:
        ansible_dotfiles_path = REPO_PATH
    else:
        if os.path.isdir(TEMP_PATH):
            os.chdir(TEMP_PATH)
            git.fetch('--all')
            git.reset('--hard', 'origin/master')
            git.pull()
        else:
            os.chdir('/tmp')
            git.clone('--recursive', 'https://github.com/carlba/ansible-dotfiles.git')

        ansible_dotfiles_path = TEMP_PATH

    ctx.obj['ansible_dotfiles_path'] = ansible_dotfiles_path


@click.command()
@click.pass_context
def list(ctx):
    """
    List all roles available in the Ansible repo

    :param ctx: The click command context
    """
    click.echo('Listing roles in {}:'.format(ctx.obj['ansible_dotfiles_path']))
    for item in os.listdir(os.path.join(ctx.obj['ansible_dotfiles_path'], 'roles')):
        print(item)


def _get_playbook_path(role, ansible_dotfiles_path):
    """

    :type ansible_dotfiles_path: str
    :type role: str
    :param role: The role that should be executed. The script will look for playbooks in the root
                 path of the repo and then in the roles/(rolename) folder.
    :param ansible_dotfiles_path: The root path of the playbook repo
    :return: The path of the playbook to execute
    """
    playbook_paths = [
        os.path.join(ansible_dotfiles_path, role + '.yml'),
        os.path.join(ansible_dotfiles_path, 'roles', role, 'playbook.yml')]

    for playbook_path in playbook_paths:
        if os.path.isfile(playbook_path):
            return playbook_path
    else:
        raise click.ClickException("The role doesn't have any playbooks")


@click.command()
@click.pass_context
@click.argument('role', nargs=1)
def play(ctx, role):

    """
    :type ctx: object
    :type role: str
    :param ctx: The click command context
    :param role: The role that should be executed.
    """

    roles_path = os.path.join(ctx.obj['ansible_dotfiles_path'], 'roles')

    # noinspection PyUnresolvedReferences
    if role not in os.listdir(roles_path) + ['dotfiles']:
        raise click.BadParameter('The role does not exist')

    vault_pass_file_path = os.path.join(HOME_PATH, '.vault_pass.txt')

    if not os.path.isfile(vault_pass_file_path):
        raise click.FileError(vault_pass_file_path, hint='A file containing the Vault '
                                                         'password is required')

    new_env = os.environ.copy()
    # noinspection PyUnresolvedReferences
    new_env['ANSIBLE_ROLES_PATH'] = os.path.join(ctx.obj['ansible_dotfiles_path'], 'roles')

    sudo_password = click.prompt('SUDO Password', type=str, hide_input=True)
    # noinspection PyUnresolvedReferences
    requirements_file = os.path.join(ctx.obj['ansible_dotfiles_path'], 'requirements.yml')

    try:
        ansible_galaxy('--roles-path', new_env['ANSIBLE_ROLES_PATH'],
                       '--role-file', requirements_file, 'install', _out=_process_output)
    except ErrorReturnCode_2 as e:
        click.echo(e.message)

    # noinspection PyUnresolvedReferences
    playbook_path = _get_playbook_path(role, ctx.obj['ansible_dotfiles_path'])
    library_path = os.path.dirname(playbook_path)

    click.echo('Executing playbook {}'.format(playbook_path))

    try:
        ansible_playbook(
            '-c', 'local', '-i', 'localhost,', '-e', 'ansible_sudo_pass={}'.format(sudo_password),
            '--module-path', os.path.join(library_path, 'library'),
            '--vault-password-file', os.path.join(HOME_PATH, '.vault_pass.txt'),
            playbook_path, _out=_process_output, _env=new_env)
    except ErrorReturnCode_2 as e:
        click.echo(e.message)


cli.add_command(list)
cli.add_command(play)

if __name__ == '__main__':
    cli()
