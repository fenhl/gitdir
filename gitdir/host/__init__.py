import sys

import abc
import subprocess

import gitdir

class Repo:
    def __init__(self, host, repo_spec):
        self.host = host
        self.spec = repo_spec

    def branch_path(self, branch=None):
        if branch is None:
            return self.path / 'master'
        return self.path / 'branch' / branch

    @property
    def path(self):
        return self.host.repo_path(self.spec)

    @property
    def stage_path(self):
        return self.path / 'stage'

class Host(abc.ABC):
    @abc.abstractmethod
    def __iter__(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def __str__(self):
        raise NotImplementedError()

    def clone(self, repo_spec):
        repo_dir = self.repo_path(repo_spec)
        if not repo_dir.exists():
            repo_dir.mkdir(parents=True)
        if (repo_dir / 'master').exists():
            self.deploy(repo_spec)
        else:
            subprocess.check_call(['git', 'clone', self.repo_remote(repo_spec), 'master'], cwd=str(repo_dir))

    def clone_stage(self, repo_spec):
        repo_dir = self.repo_path(repo_spec)
        if not repo_dir.exists():
            repo_dir.mkdir(parents=True)
        if (repo_dir / 'stage').exists():
            raise NotImplementedError('Stage already exists')
        else:
            subprocess.check_call(['git', 'clone', self.repo_remote(repo_spec, stage=True), 'stage'], cwd=str(repo_dir))

    def deploy(self, repo_spec, branch=None):
        repo = Repo(self, repo_spec)
        cwd = repo.branch_path(branch=branch)
        subprocess.check_call(['git', 'fetch', 'origin'], cwd=str(cwd))
        #TODO respect main branch
        #TODO don't reset gitignored files (or try merging and reset only if that fails)
        subprocess.check_call(['git', 'reset', '--hard', 'origin/{}'.format(branch or 'master')], cwd=str(cwd))

    @property
    def dir(self):
        return gitdir.GITDIR / str(self)

    def repo(self, repo_spec):
        return Repo(self, repo_spec)

    def repo_path(self, repo_spec):
        return self.dir / repo_spec

    @abc.abstractmethod
    def repo_remote(self, repo_spec, stage=False):
        raise NotImplementedError('Host {} does not support remotes')

    def update(self, quiet=False):
        for repo_dir in self:
            try:
                if quiet:
                    out = subprocess.check_output(['git', 'pull', '--quiet'], cwd=str(repo_dir / 'master'))
                    if out != b'':
                        sys.stdout.buffer.write(out)
                        sys.stdout.buffer.flush()
                        print('[ ** ] updated {}'.format(repo_dir))
                else:
                    print('[ ** ] updating {}'.format(repo_dir))
                    subprocess.check_call(['git', 'pull'], cwd=str(repo_dir / 'master'))
            except subprocess.CalledProcessError:
                print('[ !! ] failed to update {}'.format(repo_dir), file=sys.stderr)
                raise

def all():
    for host_dir in sorted(gitdir.GITDIR.iterdir()):
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
    elif hostname == 'gerrit.wikimedia.org':
        import gitdir.host.wikimedia
        return gitdir.host.wikimedia.Wikimedia()
    else:
        raise ValueError('Unsupported hostname: {}'.format(hostname))
