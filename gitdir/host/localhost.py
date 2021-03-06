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
        return super().clone(repo_spec, branch=branch)

    def clone_stage(self, repo_spec):
        repo_dir = self.repo_path(repo_spec)
        if not repo_dir.exists():
            raise ValueError(f'No such repo on localhost: {repo_spec!r}')
        return super().clone_stage(repo_spec)

    def repo_remote(self, repo_spec, stage=False):
        return f'/opt/git/localhost/{repo_spec}/{repo_spec}.git'
