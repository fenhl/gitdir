import gitdir.host

class GitLab(gitdir.host.Host):
    def __iter__(self):
        for user_dir in sorted(self.dir.iterdir()):
            if user_dir.is_dir():
                for repo_dir in sorted(user_dir.iterdir()):
                    if repo_dir.is_dir():
                        yield self.repo('{}/{}'.format(user_dir.name, repo_dir.name))

    def __repr__(self):
        return 'gitdir.host.gitlab.GitLab()'

    def __str__(self):
        return 'gitlab.com'

    def repo_remote(self, repo_spec, stage=False):
        user, repo_name = repo_spec.split('/')
        if stage:
            return 'git@gitlab.com:{}/{}.git'.format(user, repo_name)
        else:
            return 'https://gitlab.com/{}/{}.git'.format(user, repo_name)
