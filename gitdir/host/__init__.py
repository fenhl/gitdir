import sys

import abc
import subprocess

import gitdir

class Host(abc.ABC):
    @abc.abstractmethod
    def __iter__(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def __str__(self):
        raise NotImplementedError()

    def clone(self, repo_spec):
        raise NotImplementedError('Host {} does not support cloning'.format(self))

    @abc.abstractmethod
    def deploy(self, repo_spec, branch='master', request_time=None):
        raise NotImplementedError('Host {} does not support deploying'.format(self))

    @property
    def dir(self):
        return gitdir.GITDIR / str(self)

    def update(self, quiet=False):
        for repo_dir in self:
            if quiet:
                out = subprocess.check_output(['git', 'pull'], cwd=str(repo_dir / 'master'))
                if out != b'Already up-to-date.\n':
                    print('[ ** ] updating {}'.format(repo_dir))
                    sys.stdout.buffer.write(out)
            else:
                print('[ ** ] updating {}'.format(repo_dir))
                subprocess.check_call(['git', 'pull'], cwd=str(repo_dir / 'master'))

def all():
    for host_dir in gitdir.GITDIR.iterdir():
        if not host_dir.is_symlink() and not host_dir.name.startswith('.'): # ignore symlinks and dotfiles
            yield by_name(host_dir.name)

def by_name(hostname):
    if hostname == 'github.com':
        import gitdir.host.github
        return gitdir.host.github.GitHub()
    elif hostname == 'localhost':
        import gitdir.host.localhost
        return gitdir.host.localhost.LocalHost()
    elif hostname == 'fenhl.net':
        import gitdir.host.fenhl
        return gitdir.host.fenhl.Fenhl()
    else:
        raise ValueError('Unsupported hostname: {}'.format(hostname))
