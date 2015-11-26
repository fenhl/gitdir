import pathlib
import subprocess

import gitdir
import gitdir.host

class GitHub(gitdir.host.Host):
    def __str__(self):
        return 'github.com'

    def clone(self, repo_spec):
        user, repo_name = repo_spec.split('/')
        repo_dir = gitdir.GITDIR / str(self) / user / repo_name
        if not repo_dir.exists():
            repo_dir.mkdir(parents=True)
        if (repo_dir / 'master').exists():
            raise NotImplementedError('repo already exists') #TODO
        else:
            subprocess.check_call(['git', 'clone', 'https://github.com/{}/{}.git'.format(user, repo_name), 'master'], cwd=str(repo_dir))
