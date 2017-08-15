#!/usr/bin/python2
from __future__ import print_function

import os
import sys
import time

from sh import subl, find
import click


PROJECT_EXCLUDES = []

SUBLIME_PROJECTS_FILE = os.path.expanduser('~/.sublime_projects')


def _get_parent_basename(path):
    return os.path.basename(os.path .dirname(path))


def _update_db():
    find(os.path.expanduser('~/development'), os.path.expanduser('~/bsdev'),
                            '-name', '*.sublime-project', _out=SUBLIME_PROJECTS_FILE)


def _process_output(line):
    """
    Callback for printing output from sh commands
    :param line:
    """
    project_filename = os.path.basename(line.rstrip('\n'))

    if project_filename not in PROJECT_EXCLUDES:
        filename, extension = os.path.splitext(project_filename)
    print(filename)


def _get_projects_on_disk():
    last_modified_epoch_time = os.path.getmtime(SUBLIME_PROJECTS_FILE)
    epoch_time = int(time.time())

    if (epoch_time - last_modified_epoch_time) > 300:
        _update_db()

    with open(SUBLIME_PROJECTS_FILE) as project_file:
        projects_on_disk = project_file.readlines()

    return projects_on_disk


@click.command()
@click.argument('project', nargs=-1)
@click.option('--update/--no-update', default=False)
def sublime_projects(project, update):

    if update:
        _update_db()
        sys.exit()

    if not project:
        for project_on_disk in _get_projects_on_disk():
            _process_output(project_on_disk)
    else:
        for project_on_disk in _get_projects_on_disk():
            if project[0] == _get_parent_basename(project_on_disk):
                subl(os.path.dirname(project_on_disk))


if __name__ == '__main__':
    sublime_projects()
