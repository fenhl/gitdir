import pathlib
import subprocess

import gitdir
import gitdir.host

class Fenhl(gitdir.host.Host):
    def __iter__(self):
        yield from self.dir.iterdir()

    def __str__(self):
        return 'fenhl.net'

    def clone(self, repo_spec):
        repo_name = repo_spec
        repo_dir = self.dir / repo_name
        if not repo_dir.exists():
            repo_dir.mkdir(parents=True)
        if (repo_dir / 'master').exists():
            raise NotImplementedError('repo already exists') #TODO
        else:
            subprocess.check_call(['git', 'clone', 'fenhl@fenhl.net:/opt/git/localhost/{repo_name}/{repo_name}.git'.format(repo_name=repo_name), 'master'], cwd=str(repo_dir))
