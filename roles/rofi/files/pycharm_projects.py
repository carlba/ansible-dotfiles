#!/usr/bin/python2
from __future__ import print_function

import click
import os
from sh import locate, pycharm

PROJECT_EXCLUDES = ['hoist-non-react-statics', 'multi-stage-sourcemap', 'corslite']


def _process_output(line):
    """
    Callback for printing output from sh commands
    :param line:
    """
    print(line, end="")


def _get_parent_basename(path):
    return os.path.basename(os.path.dirname(path))


@click.command()
@click.argument('project', nargs=-1)
def sublime_projects(project):
    if not project:
        projects_on_disk = locate('-r', '\.idea$').split()

        basenames = set([_get_parent_basename(project_on_disk)
                         for project_on_disk in projects_on_disk])

        filtered_basenames = {basename for basename in basenames if
                              basename not in PROJECT_EXCLUDES}

        for filtered_basename in filtered_basenames:
            print(filtered_basename)

    else:
        projects_on_disk = locate('-r', '\.idea$').split()

        basenames = {_get_parent_basename(project_on_disk): os.path.dirname(project_on_disk)
                     for project_on_disk in projects_on_disk}

        pycharm(basenames[project[0]], _bg=True)

if __name__ == '__main__':
    sublime_projects()
