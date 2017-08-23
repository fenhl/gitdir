import subprocess

import gitdir.host

class Fenhl(gitdir.host.Host):
    def __iter__(self):
        yield from sorted(self.dir.iterdir())

    def __str__(self):
        return 'fenhl.net'

    def repo_remote(self, repo_spec, stage=False):
        return 'fenhl@fenhl.net:/opt/git/localhost/{}/{}.git'.format(repo_spec, repo_spec)
