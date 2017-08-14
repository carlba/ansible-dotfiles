#!/usr/bin/python2
from __future__ import print_function

import click
import os
from sh import locate, subl


def _process_output(line):
    """
    Callback for printing output from sh commands
    :param line:
    """
    sublime_project_filename = os.path.basename(line.rstrip('\n'))
    filename, extension = os.path.splitext(sublime_project_filename)

    print(filename)


@click.command()
@click.argument('project', nargs=-1)
def sublime_projects(project):
    if not project:
        locate('sublime-project', _out=_process_output)
    else:
        projects_on_disk = locate('sublime-project')
        found_project = [project_on_disk for project_on_disk in projects_on_disk.split()
                         if project[0] in project_on_disk]

        subl(found_project)



if __name__ == '__main__':
    sublime_projects()
