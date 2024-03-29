#!/usr/bin/env python3

"""Utility for maintaining gitdirs.

Usage:
  gitdir clone <host> <repo_spec> [<branch>]
  gitdir clone-stage <host> <repo_spec>
  gitdir deploy <host> <repo_spec> [<branch>]
  gitdir path <host> <repo_spec> [<branch>]
  gitdir path-stage <host> <repo_spec>
  gitdir [options] update [<host>]
  gitdir -h | --help
  gitdir --version

Options:
  -h, --help   Print this message and exit.
  -q, --quiet  Only produce output for repos that have been changed.
  --version    Print version info and exit.
"""

import sys

sys.path.append('/opt/py')

import docopt
import pathlib
import subprocess

import gitdir.host

def parse_version_string():
    path = pathlib.Path(__file__).resolve().parent.parent # go up one level, from repo/gitdir/__main__.py to repo, where README.md is located
    version = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=str(path)).decode('utf-8').strip('\n')
    if version in ('main', 'master'):
        with (path / 'README.md').open() as readme:
            for line in readme.read().splitlines():
                if line.startswith('This is gitdir version '):
                    return line.split(' ')[4]
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], cwd=str(path)).decode('utf-8').strip('\n')

__version__ = str(parse_version_string())

if __name__ == '__main__':
    arguments = docopt.docopt(__doc__, version='gitdir ' + __version__)
    if arguments['clone']:
        gitdir.host.by_name(arguments['<host>']).clone(arguments['<repo_spec>'], branch=arguments['<branch>'])
    elif arguments['clone-stage']:
        gitdir.host.by_name(arguments['<host>']).clone_stage(arguments['<repo_spec>'])
    elif arguments['deploy']:
        gitdir.host.by_name(arguments['<host>']).deploy(arguments['<repo_spec>'], branch=arguments['<branch>'])
    elif arguments['path']:
        print(gitdir.host.by_name(arguments['<host>']).repo(arguments['<repo_spec>']).branch_path(arguments['<branch>']))
    elif arguments['path-stage']:
        print(gitdir.host.by_name(arguments['<host>']).repo(arguments['<repo_spec>']).stage_path)
    elif arguments['update']:
        if arguments['<host>']:
            gitdir.host.by_name(arguments['<host>']).update(quiet=arguments['--quiet'])
        else:
            for host in gitdir.host.all():
                host.update(quiet=arguments['--quiet'])
    else:
        raise NotImplementedError('unknown subcommand')
