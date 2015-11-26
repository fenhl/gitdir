#!/usr/bin/env python3

"""Utility for maintaining gitdirs.

Usage:
  gitdir clone <host> <repo_spec>...
  gitdir -h | --help
  gitdir --version

Options:
  -h, --help  Print this message and exit.
  --version   Print version info and exit.
"""

import docopt
import pathlib
import subprocess

import gitdir.host

def parse_version_string():
    path = pathlib.Path(__file__).resolve().parent.parent # go up one level, from repo/gitdir/__main__.py to repo, where README.md is located
    version = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=str(path)).decode('utf-8').strip('\n')
    if version == 'master':
        with (path / 'README.md').open() as readme:
            for line in readme.read().splitlines():
                if line.startswith('This is gitdir version '):
                    return line.split(' ')[4]
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], cwd=str(path)).decode('utf-8').strip('\n')

__version__ = str(parse_version_string())

if __name__ == '__main__':
    arguments = docopt.docopt(__doc__, version='gitdir ' + __version__)
    if arguments['clone']:
        for repo_spec in arguments['<repo_spec>']:
            gitdir.host.by_name(arguments['<host>']).clone(repo_spec)
    else:
        raise NotImplementedError('unknown subcommand')
