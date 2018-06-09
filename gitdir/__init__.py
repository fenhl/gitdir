import os
import pathlib

GLOBAL_GITDIR = pathlib.Path('/opt/git')
LOCAL_GITDIR = pathlib.Path.home() / 'git'

if 'GITDIR' in is.environ:
    GITDIR = pathlib.Path(os.environ['GITDIR'])
elif LOCAL_GITDIR.exists() and not GLOBAL_GITDIR.exists(): #TODO check permissions
    GITDIR = LOCAL_GITDIR
else:
    GITDIR = GLOBAL_GITDIR
