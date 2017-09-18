import gitdir.host

class Wikimedia(gitdir.host.Host):
    def __iter__(self):
        yield from sorted((self.dir / 'mediawiki' / 'extensions').iterdir())

    def __str__(self):
        return 'gerrit.wikimedia.org'

    def repo_path(self, repo_spec):
        return self.dir / 'mediawiki' / 'extensions' / repo_spec

    def repo_remote(self, repo_spec, stage=False):
        if stage:
            raise NotImplementedError('Stages not implemented for Wikimedia host')
        else:
            return 'https://gerrit.wikimedia.org/r/p/mediawiki/extensions/{}.git'.format(repo_spec)
