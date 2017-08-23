import subprocess

import gitdir.host

class LocalHost(gitdir.host.Host):
    def __iter__(self):
        yield from sorted(self.dir.iterdir())

    def __str__(self):
        return 'localhost'

    def clone(self, repo_spec):
        repo_dir = self.repo_path(repo_spec)
        if not repo_dir.exists():
            raise ValueError('No such repo on localhost: {!r}'.format(repo_spec))
        return super().clone(repo_spec)

    def clone_stage(self, repo_spec):
        repo_dir = self.repo_path(repo_spec)
        if not repo_dir.exists():
            raise ValueError('No such repo on localhost: {!r}'.format(repo_spec))
        return super().clone(repo_spec)

    def repo_remote(self, repo_spec, stage=False):
        return '/opt/git/localhost/{}/{}.git'.format(repo_spec, repo_spec)
