**gitdir** is a system that helps you keep your git repositories organized. It is *not* a git workflow, and works with different (but not all) workflows. Gitdir is the successor to [hubdir](https://github.com/fenhl/hubdir), generalized to allow working with repositories that are not hosted on github.

This is gitdir version 2.0.3 ([semver](http://semver.org/)). The versioned API is described below, in the section *The system*.

# The system

This section describes the gitdir system.

## The directories

In the gitdir system, all git repos are organized within the *git directories*, or *gitdirs*. There are two kinds of gitdir:

1.  the global gitdir at `/opt/git`, and
2.  the local gitdirs at `~/git`. Each user can have their own local gitdir.

The global gitdir will be used by default, while the user's local gitdir is used only for staging and when the global gitdir is inaccessible.

## Directory structure

A gitdir contains subdirectories for any host from which repositories are cloned. The way repositories are organized within the host directory is defined individually for each host. For example, `github.com` organizes repositories by github username and repo name, so that the directory for this repo would be located at `/opt/git/github.com/fenhl/gitdir`.

Four different kinds of repos may reside within a repo directory:

1.  Master repos, located at `<repodir>/master`. These track [the default branch](https://help.github.com/articles/setting-the-default-branch) from the remote and should always stay clean.
2.  Branches, located at `<repodir>/branch/<branch>`. These work like the master repos, except they track a different remote branch.
3.  Stages, located at `<repodir>/stage`. These have more loose restrictions and are where any work happens.
4.  Bare repos, located at `<repodir>/<reponame>.git`. These are created with `git init --bare`, and should be used as the remote when hosting locally (`/opt/git/localhost`).

## Repo setup

Within a repo, the following rules should be, well, followed:

*   All github repos have the default `origin` remote set up as follows:
    *   For master and branch repos, `https://github.com/<user>/<reponame>.git`
    *   For stage repos, `git@github.com:<user>/<reponame>.git`
*   Master and branch repos have no other remotes. For stages, do whatever works best for your git workflow.
*   In multi-user environments, the global gitdir and everything under it should be owned by a group named `git` and be group read-writeable.
