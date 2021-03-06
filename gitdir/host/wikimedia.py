import gitdir.host

class Wikimedia(gitdir.host.Host):
    def __iter__(self):
        for repo_dir in sorted((self.dir / 'mediawiki' / 'extensions').iterdir()):
            if repo_dir.is_dir():
                yield self.repo(repo_dir.name)

    def __repr__(self):
        return 'gitdir.host.wikimedia.Wikimedia()'

    def __str__(self):
        return 'gerrit.wikimedia.org'

    def repo_path(self, repo_spec):
        return self.dir / 'mediawiki' / 'extensions' / repo_spec

    def repo_remote(self, repo_spec, stage=False):
        if stage:
            raise NotImplementedError('Stages not implemented for Wikimedia host')
        else:
            return f'https://gerrit.wikimedia.org/r/p/mediawiki/extensions/{repo_spec}.git'
