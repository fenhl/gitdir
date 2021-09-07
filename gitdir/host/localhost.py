import subprocess
import gitdir.host

class LocalHost(gitdir.host.Host):
    def __iter__(self):
        for repo_dir in sorted(self.dir.iterdir()):
            if repo_dir.is_dir():
                yield self.repo(repo_dir.name)

    def __repr__(self):
        return 'gitdir.host.localhost.LocalHost()'

    def __str__(self):
        return 'localhost'

    def clone(self, repo_spec, *, branch=None):
        repo_dir = self.repo_path(repo_spec)
        if not repo_dir.exists():
            raise ValueError(f'No such repo on localhost: {repo_spec!r}')
        if branch is None:
            branch_dir = repo_dir / 'master' #TODO use 'main' instead
        else:
            branch_dir = repo_dir / 'branch' / branch
        if branch_dir.exists():
            self.deploy(repo_spec, branch=branch)
        else:
            if branch is None:
                branch = subprocess.run(['git', 'symbolic-ref', 'HEAD'], cwd=repo_dir / f'{repo_spec}.git', stdout=subprocess.PIPE, encoding='utf-8', check=True).stdout.strip().split('/')[-1]
            subprocess.run(['git', 'worktree', 'add', str(branch_dir), branch], cwd=repo_dir / f'{repo_spec}.git', check=True)

    def clone_stage(self, repo_spec):
        repo_dir = self.repo_path(repo_spec)
        if not repo_dir.exists():
            raise ValueError(f'No such repo on localhost: {repo_spec!r}')
        return super().clone_stage(repo_spec)

    def deploy(self, repo_spec, branch=None):
        #TODO also support non-worktree checkouts left over from older versions
        cwd = gitdir.host.Repo(self, repo_spec).branch_path(branch=branch)
        subprocess.run(['git', 'reset', '--hard'], cwd=cwd, check=True)
        #TODO also run deploy hooks once implemented

    def repo_remote(self, repo_spec, stage=False):
        return f'/opt/git/localhost/{repo_spec}/{repo_spec}.git'
