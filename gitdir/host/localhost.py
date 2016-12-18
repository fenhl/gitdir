import subprocess

import gitdir.host

class LocalHost(gitdir.host.Host):
    def __iter__(self):
        yield from sorted(self.dir.iterdir())

    def __str__(self):
        return 'localhost'

    def clone(self, repo_spec):
        repo_name = repo_spec
        repo_dir = self.dir / repo_name
        if not repo_dir.exists():
            raise ValueError('No such repo on localhost: {!r}'.format(repo_spec))
        if (repo_dir / 'master').exists():
            self.deploy(repo_spec)
        else:
            subprocess.check_call(['git', 'clone', '/opt/git/localhost/{repo_name}/{repo_name}.git'.format(repo_name=repo_name), 'master'], cwd=str(repo_dir))

    def clone_stage(self, repo_spec):
        repo_name = repo_spec
        repo_dir = self.dir / repo_name
        if not repo_dir.exists():
            raise ValueError('No such repo on localhost: {!r}'.format(repo_spec))
        if (repo_dir / 'stage').exists():
            raise NotImplementedError('Stage already exists')
        else:
            subprocess.check_call(['git', 'clone', '/opt/git/localhost/{repo_name}/{repo_name}.git'.format(repo_name=repo_name), 'stage'], cwd=str(repo_dir))

    def deploy(self, repo_spec, branch='master'):
        repo_name = repo_spec
        if branch == 'master' or branch is None:
            cwd = self.dir / repo_name / 'master'
        else:
            cwd = self.dir / repo_name / 'branch' / branch
        subprocess.check_call(['git', 'fetch', 'origin'], cwd=str(cwd))
        subprocess.check_call(['git', 'reset', '--hard', 'origin/{}'.format(branch or 'master')], cwd=str(cwd)) #TODO don't reset gitignored files (or try merging and reset only if that fails)
