import subprocess

import gitdir.host

class Wikimedia(gitdir.host.Host):
    def __iter__(self):
        yield from sorted((self.dir / 'mediawiki' / 'extensions').iterdir())

    def __str__(self):
        return 'gerrit.wikimedia.org'

    def clone(self, repo_spec):
        repo_name = repo_spec
        repo_dir = self.dir / 'mediawiki' / 'extensions' / repo_name
        if not repo_dir.exists():
            repo_dir.mkdir(parents=True)
        if (repo_dir / 'master').exists():
            raise NotImplementedError('repo already exists') #TODO
        else:
            subprocess.check_call(['git', 'clone', 'https://gerrit.wikimedia.org/r/p/mediawiki/extensions/{repo_name}.git'.format(repo_name=repo_name), 'master'], cwd=str(repo_dir))

    def deploy(self, repo_spec, branch='master'):
        repo_name = repo_spec
        if branch == 'master' or branch is None:
            cwd = self.dir / 'mediawiki' / 'extensions' / repo_name / 'master'
        else:
            cwd = self.dir / 'mediawiki' / 'extensions' / repo_name / 'branch' / branch
        subprocess.check_call(['git', 'fetch', 'origin'], cwd=str(cwd))
        subprocess.check_call(['git', 'reset', '--hard', 'origin/{}'.format(branch or 'master')], cwd=str(cwd)) #TODO don't reset gitignored files (or try merging and reset only if that fails)
