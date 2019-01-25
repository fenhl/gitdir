import sys

import abc
import contextlib
import subprocess

import gitdir

class Repo:
    def __init__(self, host, repo_spec):
        self.host = host
        self.spec = repo_spec

    @staticmethod
    def lookup(path):
        for host in all():
            with contextlib.suppress(LookupError):
                return host.lookup(path)
        else:
            raise LookupError('Path is not a repo dir')

    def __repr__(self):
        return 'gitdir.host.Repo({!r}, {!r})'.format(self.host, self.spec)

    def __str__(self):
        return '{}/{}'.format(self.host, self.spec)

    def branch_path(self, branch=None):
        if branch is None:
            return self.path / 'master'
        #TODO respect main branch
        return self.path / 'branch' / branch

    def clone(self, *, branch=None):
        return self.host.clone(self.spec, branch=branch)

    def clone_stage(self):
        return self.host.clone_stage(self.spec)

    def deploy(self, branch=None):
        return self.host.deploy(self.spec, branch=branch)

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
    def __repr__(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def __str__(self):
        raise NotImplementedError()

    def clone(self, repo_spec, *, branch=None):
        repo = Repo(self, repo_spec)
        branch_dir = repo.branch_path(branch)
        if branch_dir.exists():
            self.deploy(repo_spec, branch=branch)
        else:
            branch_dir.parent.mkdir(parents=True, exist_ok=True)
            subprocess.check_call(['git', 'clone'] + ([] if branch is None else ['--branch={}'.format(branch)]) + [self.repo_remote(repo_spec), branch_dir.name], cwd=str(branch_dir.parent))

    def clone_stage(self, repo_spec):
        self.clone(repo_spec)
        repo_dir = self.repo_path(repo_spec)
        if (repo_dir / 'stage').exists():
            raise NotImplementedError('Stage already exists')
        else:
            subprocess.check_call(['git', 'clone', self.repo_remote(repo_spec, stage=True), 'stage'], cwd=str(repo_dir))

    def deploy(self, repo_spec, branch=None):
        repo = Repo(self, repo_spec)
        cwd = repo.branch_path(branch=branch)
        subprocess.check_call(['git', 'fetch', 'origin'], cwd=str(cwd))
        # respect main branch
        if branch is None:
            all_branches = subprocess.run(['git', 'branch', '-a'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=True, cwd=str(cwd)).stdout.decode('utf-8').splitlines()
            for line in all_branches:
                if line.startswith('  remotes/origin/HEAD -> origin/'):
                    branch = line[len('  remotes/origin/HEAD -> origin/'):]
                    break
            else:
                branch = 'master'
        #TODO don't reset gitignored files (or try merging and reset only if that fails)
        try:
            subprocess.check_call(['git', 'reset', '--hard', 'origin/{}'.format(branch)], cwd=str(cwd))
        except subprocess.CalledProcessError:
            subprocess.check_call(['git', 'pull'], cwd=str(cwd))

    @property
    def dir(self):
        result = gitdir.GITDIR / str(self)
        if result.exists():
            result = result.resolve()
        return result

    def lookup(self, path):
        def cmp_paths(left, right):
            if left == right:
                return True
            if left.exists():
                if left.resolve() == right:
                    return True
            if right.exists():
                if left == right.resolve():
                    return True
            if left.exists() and right.exists():
                if left.resolve() == right.resolve():
                    return True
            return False

        for repo in self:
            if cmp_paths(repo.path, path):
                return repo, 'base'
            elif cmp_paths(repo.branch_path(), path):
                return repo, 'master'
            elif cmp_paths(repo.stage_path, path):
                return repo, 'stage'
            #TODO support branches
        else:
            raise LookupError('Path is not a repo dir in {}'.format(self))

    def repo(self, repo_spec):
        return Repo(self, repo_spec)

    def repo_path(self, repo_spec):
        result = self.dir / repo_spec
        if result.exists():
            result = result.resolve()
        return result

    @abc.abstractmethod
    def repo_remote(self, repo_spec, stage=False):
        raise NotImplementedError('Host {} does not support remotes')

    def update(self, quiet=False):
        for repo in self:
            try:
                if quiet:
                    out = subprocess.check_output(['git', 'pull', '--quiet'], cwd=str(repo.branch_path())) #TODO (Python 3.6) remove str wrapper
                    if out != b'':
                        sys.stdout.buffer.write(out)
                        sys.stdout.buffer.flush()
                        print('[ ** ] updated {}'.format(repo))
                else:
                    print('[ ** ] updating {}'.format(repo))
                    subprocess.check_call(['git', 'pull'], cwd=str(repo.branch_path())) #TODO (Python 3.6) remove str wrapper
            except subprocess.CalledProcessError:
                print('[ !! ] failed to update {}'.format(repo), file=sys.stderr)
                raise

def all():
    for host_dir in sorted(gitdir.GITDIR.iterdir()):
        if not host_dir.is_symlink() and not host_dir.name.startswith('.'): # ignore symlinks and dotfiles
            yield by_name(host_dir.name)

def by_name(hostname):
    if hostname == 'github.com':
        import gitdir.host.github
        return gitdir.host.github.GitHub()
    elif hostname == 'gitlab.com':
        import gitdir.host.gitlab
        return gitdir.host.gitlab.GitLab()
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
