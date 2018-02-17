import gitdir.host

class Fenhl(gitdir.host.Host):
    def __iter__(self):
        for repo_dir in sorted(self.dir.iterdir()):
            if repo_dir.is_dir():
                yield self.repo(repo_dir.name)

    def __repr__(self):
        return 'gitdir.host.fenhl.Fenhl()'

    def __str__(self):
        return 'fenhl.net'

    def repo_remote(self, repo_spec, stage=False):
        return 'fenhl@fenhl.net:/opt/git/localhost/{}/{}.git'.format(repo_spec, repo_spec)
