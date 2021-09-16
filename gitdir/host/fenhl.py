import socket

import gitdir.host
import gitdir.host.localhost

class Fenhl(gitdir.host.Host):
    def __new__(cls):
        if socket.getfqdn() == 'mercredi.fenhl.net':
            return gitdir.host.localhost.LocalHost()
        else:
            return super().__new__(cls)

    def __iter__(self):
        for repo_dir in sorted(self.dir.iterdir()):
            if repo_dir.is_dir():
                yield self.repo(repo_dir.name)

    def __repr__(self):
        return 'gitdir.host.fenhl.Fenhl()'

    def __str__(self):
        return 'fenhl.net'

    def repo_remote(self, repo_spec, stage=False):
        return f'fenhl@fenhl.net:/opt/git/localhost/{repo_spec}/{repo_spec}.git'
