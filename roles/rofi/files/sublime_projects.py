#!/usr/bin/python2
from __future__ import print_function


import os
from datetime import datetime
import time

from sh import locate, subl, find
import click


SUBLIME_PROJECTS_FILE = os.path.expanduser('~/.sublime_projects')


def _process_output(line):
    """
    Callback for printing output from sh commands
    :param line:
    """

    sublime_project_filename = os.path.basename(line.rstrip('\n'))
    filename, extension = os.path.splitext(sublime_project_filename)
    print(filename)


def _get_projects_on_disk():
    last_modified_epoch_time = os.path.getmtime(SUBLIME_PROJECTS_FILE)
    epoch_time = int(time.time())

    if (epoch_time - last_modified_epoch_time) > 300:
        print("Updating")

        find(os.path.expanduser('~/development'), os.path.expanduser('~/bsdev'),
                                '-name', '*.sublime-project', _out=SUBLIME_PROJECTS_FILE)

    with open(SUBLIME_PROJECTS_FILE) as project_file:
        projects_on_disk = project_file.readlines()
    return projects_on_disk


def _get_parent_basename(path):
    return os.path.basename(os.path.dirname(path))


@click.command()
@click.argument('project', nargs=-1)
def sublime_projects(project):
    if not project:
        for project_on_disk in _get_projects_on_disk():
            _process_output(project_on_disk)

    else:
        for project_on_disk in _get_projects_on_disk():
            if project[0] == _get_parent_basename(project_on_disk):
                subl(os.path.dirname(project_on_disk))

        subl(project_on_disk)


if __name__ == '__main__':
    sublime_projects()
