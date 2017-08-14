#!/usr/bin/python2
from __future__ import print_function

import os
import time

import click
from sh import locate, pycharm, find


PROJECT_EXCLUDES = ['hoist-non-react-statics', 'multi-stage-sourcemap', 'corslite',
                    'jsLinters', 'inspectionProfiles', 'lessc', 'dictionaries',
                    'libraries']

PYCHARM_PROJECTS_FILE = os.path.expanduser('~/.sublime_projects')

def _get_parent_basename(path):
    return os.path.basename(os.path.dirname(path))

def _process_output(line):
    """
    Callback for printing output from sh commands
    :param line:
    """
    project_filename = _get_parent_basename(line.rstrip('\n'))

    if project_filename not in PROJECT_EXCLUDES:
        print(project_filename)



def _get_projects_on_disk():
    last_modified_epoch_time = os.path.getmtime(PYCHARM_PROJECTS_FILE)
    epoch_time = int(time.time())

    if (epoch_time - last_modified_epoch_time) > 300:
        print("Updating")

        find(os.path.expanduser('~/development'), os.path.expanduser('~/bsdev'),
                                '-type', 'd', '-name', '.idea', _out=PYCHARM_PROJECTS_FILE)

    with open(PYCHARM_PROJECTS_FILE) as project_file:
        projects_on_disk = project_file.readlines()

    return projects_on_disk



@click.command()
@click.argument('project', nargs=-1)
def sublime_projects(project):
    if not project:
        for project_on_disk in _get_projects_on_disk():
            _process_output(project_on_disk)
    else:
        for project_on_disk in _get_projects_on_disk():
            if project[0] == _get_parent_basename(project_on_disk):
                pycharm(os.path.dirname(project_on_disk), _bg=True)

if __name__ == '__main__':
    sublime_projects()
