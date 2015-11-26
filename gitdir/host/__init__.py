import abc

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
            subprocess.check_call(['git', 'pull'], cwd=str(repo_dir / 'master'))

def all():
    for host_dir in gitdir.GITDIR.iterdir():
        yield by_name(host_dir.name)

def by_name(hostname):
    if hostname == 'github.com':
        import gitdir.host.github
        return gitdir.host.github.GitHub()
    else:
        raise ValueError('Unsupported hostname: {}'.format(hostname))
