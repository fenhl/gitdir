import github # PyPI: PyGithub

import gitdir.host

class GitHub(gitdir.host.Host):
    def __iter__(self):
        for user_dir in sorted(self.dir.iterdir()):
            if user_dir.is_dir():
                for repo_dir in sorted(user_dir.iterdir()):
                    if repo_dir.is_dir():
                        yield self.repo(f'{user_dir.name}/{repo_dir.name}')

    def __repr__(self):
        return 'gitdir.host.github.GitHub()'

    def __str__(self):
        return 'github.com'

    def repo_remote(self, repo_spec, stage=False):
        user, repo_name = repo_spec.split('/')
        if stage:
            return f'git@github.com:{user}/{repo_name}.git'
        else:
            try:
                github.Github().get_user(user).get_repo(repo_name)
            except github.GithubException:
                return f'git@github.com:{user}/{repo_name}.git'
            else:
                return f'https://github.com/{user}/{repo_name}.git'
