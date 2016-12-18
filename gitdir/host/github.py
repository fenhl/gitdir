import subprocess

import gitdir.host

class GitHub(gitdir.host.Host):
    def __iter__(self):
        for user_dir in sorted(self.dir.iterdir()):
            yield from sorted(user_dir.iterdir())

    def __str__(self):
        return 'github.com'

    def clone(self, repo_spec):
        user, repo_name = repo_spec.split('/')
        repo_dir = self.dir / user / repo_name
        if not repo_dir.exists():
            repo_dir.mkdir(parents=True)
        if (repo_dir / 'master').exists():
            self.deploy(repo_spec)
        else:
            subprocess.check_call(['git', 'clone', 'https://github.com/{}/{}.git'.format(user, repo_name), 'master'], cwd=str(repo_dir))

    def clone_stage(self, repo_spec):
        user, repo_name = repo_spec.split('/')
        repo_dir = self.dir / user / repo_name
        if not repo_dir.exists():
            repo_dir.mkdir(parents=True)
        if (repo_dir / 'stage').exists():
            raise NotImplementedError('Stage already exists')
        else:
            subprocess.check_call(['git', 'clone', 'git@github.com:{}/{}.git'.format(user, repo_name), 'stage'], cwd=str(repo_dir))

    def deploy(self, repo_spec, branch='master'):
        user, repo_name = repo_spec.split('/')
        if branch == 'master' or branch is None:
            cwd = self.dir / user / repo_name / 'master'
        else:
            cwd = self.dir / user / repo_name / 'branch' / branch
        subprocess.check_call(['git', 'fetch', 'origin'], cwd=str(cwd))
        subprocess.check_call(['git', 'reset', '--hard', 'origin/{}'.format(branch or 'master')], cwd=str(cwd)) #TODO don't reset gitignored files (or try merging and reset only if that fails)
