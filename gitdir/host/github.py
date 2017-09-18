import gitdir.host

class GitHub(gitdir.host.Host):
    def __iter__(self):
        for user_dir in sorted(self.dir.iterdir()):
            yield from sorted(user_dir.iterdir())

    def __str__(self):
        return 'github.com'

    def repo_remote(self, repo_spec, stage=False):
        user, repo_name = repo_spec.split('/')
        if stage:
            return 'git@github.com:{}/{}.git'.format(user, repo_name)
        else:
            return 'https://github.com/{}/{}.git'.format(user, repo_name)
