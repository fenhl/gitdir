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

    @property
    def dir(self):
        return gitdir.GITDIR / str(self)

    def update(self):
        for repo_dir in self:
            print('[ ** ] updating {}'.format(repo_dir))
            subprocess.check_call(['git', 'pull'], cwd=str(repo_dir / 'master'))

def all():
    for host_dir in gitdir.GITDIR.iterdir():
        if not host_dir.name.startswith('.'): # ignore dotfiles
            yield by_name(host_dir.name)

def by_name(hostname):
    if hostname == 'fenhl.net':
        import gitdir.host.fenhl
        return gitdir.host.fenhl.Fenhl()
    elif hostname == 'github.com':
        import gitdir.host.github
        return gitdir.host.github.GitHub()
    else:
        raise ValueError('Unsupported hostname: {}'.format(hostname))
