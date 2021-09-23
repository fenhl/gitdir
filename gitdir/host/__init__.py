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
        return f'gitdir.host.Repo({self.host!r}, {self.spef!r})'

    def __str__(self):
        return f'{self.host}/{self.spec}'

    def branch_path(self, branch=None):
        if branch is None:
            return self.path / 'master' #TODO use main instead
        return self.path / 'branch' / branch

    @property
    def branches(self):
        if (self.path / 'branch').exists():
            for branch_path in (self.path / 'branch').iterdir():
                if branch_path.is_dir():
                    yield branch_path.name

    def clone(self, *, branch=None):
        return self.host.clone(self.spec, branch=branch)

    def clone_stage(self):
        return self.host.clone_stage(self.spec)

    def deploy(self, branch=None, *, quiet=False):
        return self.host.deploy(self.spec, branch=branch, quiet=quiet)

    def deploy_all(self, *, quiet=False):
        self.deploy(quiet=quiet)
        for branch in self.branches:
            self.deploy(branch, quiet=quiet)

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
            subprocess.check_call(['git', 'clone', '--recurse-submodules'] + ([] if branch is None else [f'--branch={branch}']) + [self.repo_remote(repo_spec), branch_dir.name], cwd=str(branch_dir.parent))

    def clone_stage(self, repo_spec):
        self.clone(repo_spec)
        repo_dir = self.repo_path(repo_spec)
        if (repo_dir / 'stage').exists():
            raise NotImplementedError('Stage already exists')
        else:
            subprocess.check_call(['git', 'clone', '--recurse-submodules', self.repo_remote(repo_spec, stage=True), 'stage'], cwd=repo_dir)

    def deploy(self, repo_spec, branch=None, *, quiet=False):
        quiet_arg = ['--quiet'] if quiet else []
        repo = Repo(self, repo_spec)
        cwd = repo.branch_path(branch=branch)
        subprocess.check_call(['git', 'fetch', *quiet_arg, 'origin'], cwd=cwd)
        # respect main branch
        if branch is None:
            all_branches = subprocess.run(['git', 'branch', '-a'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=True, cwd=cwd).stdout.decode('utf-8').splitlines()
            for line in all_branches:
                if line.startswith('  remotes/origin/HEAD -> origin/'):
                    branch = line[len('  remotes/origin/HEAD -> origin/'):]
                    break
            else:
                branch = 'master'
        #TODO don't reset gitignored files (or try merging and reset only if that fails)
        if subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], stdout=subprocess.PIPE, check=True, cwd=cwd).stdout.decode('utf-8').strip() != 'HEAD': # don't reploy if in “detached HEAD” state (tag repos)
            try:
                subprocess.check_call(['git', 'reset', *quiet_arg, '--hard', f'origin/{branch}'], cwd=cwd)
            except subprocess.CalledProcessError:
                subprocess.check_call(['git', 'pull', *quiet_arg], cwd=cwd)

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
            raise LookupError(f'Path is not a repo dir in {self}')

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
                if not quiet:
                    print(f'[ ** ] updating {repo}')
                repo.deploy_all(quiet=quiet)
            except subprocess.CalledProcessError:
                print(f'[ !! ] failed to update {repo}', file=sys.stderr)
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
        raise ValueError(f'Unsupported hostname: {hostname}')
