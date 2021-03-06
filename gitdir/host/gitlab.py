import gitdir.host

class GitLab(gitdir.host.Host):
    def __iter__(self):
        for user_dir in sorted(self.dir.iterdir()):
            if user_dir.is_dir():
                for repo_dir in sorted(user_dir.iterdir()):
                    if repo_dir.is_dir():
                        yield self.repo(f'{user_dir.name}/{repo_dir.name}')

    def __repr__(self):
        return 'gitdir.host.gitlab.GitLab()'

    def __str__(self):
        return 'gitlab.com'

    def repo_remote(self, repo_spec, stage=False):
        user, repo_name = repo_spec.split('/')
        if stage:
            return f'git@gitlab.com:{user}/{repo_name}.git'
        else:
            return f'https://gitlab.com/{user}/{repo_name}.git'
