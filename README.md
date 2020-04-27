![By ULHPC](https://img.shields.io/badge/by-ULHPC-blue.svg) [![gitlab](https://img.shields.io/badge/git-gitlab-lightgray.svg)](https://gitlab.uni.lu/www/ulhpc-docs) [![Issues](https://img.shields.io/badge/issues-gitlab-green.svg)](https://gitlab.uni.lu/www/ulhpc-docs/issues)

         _    _ _      _    _ _____   _____   _______        _           _           _   _____                 
        | |  | | |    | |  | |  __ \ / ____| |__   __|      | |         (_)         | | |  __ \                
        | |  | | |    | |__| | |__) | |         | | ___  ___| |__  _ __  _  ___ __ _| | | |  | | ___   ___ ___ 
        | |  | | |    |  __  |  ___/| |         | |/ _ \/ __| '_ \| '_ \| |/ __/ _` | | | |  | |/ _ \ / __/ __|
        | |__| | |____| |  | | |    | |____     | |  __/ (__| | | | | | | | (__ (_| | | | |__| | (_) | (__\__ \
         \____/|______|_|  |_|_|     \_____|    |_|\___|\___|_| |_|_| |_|_|\___\__,_|_| |_____/ \___/ \___|___/
                                                                                                               
                                                                                                               
       Copyright (c) 2020 UL HPC Team <hpc-team@uni.lu>

ULHPC Technical Documentation, based on mkdocs

## Installation / Repository Setup

This repository is hosted on [Gitlab @ Uni.lu](https://gitlab.uni.lu/www/ulhpc-docs).

* Git interactions with this repository (push, pull etc.) are performed over SSH using the port 8022
* To clone this repository, proceed as follows (adapt accordingly):

```bash
$> mkdir -p ~/git/gitlab.uni.lu/www/
$> cd ~/git/gitlab.uni.lu/www/
$> git clone ssh://git@gitlab.uni.lu:8022/www/ulhpc-docs.git
```


**`/!\ IMPORTANT`**: Once cloned, initiate your local copy of the repository by running:

```bash
$> cd ulhpc-docs
$> make setup
```

This will initiate the [Git submodules of this repository](.gitmodules) and setup the [git flow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) layout for this repository. Later on, you can update your local branches by running:

     $> make up

If upon pulling the repository, you end in a state where another collaborator have upgraded the Git submodules for this repository, you'll end in a dirty state (as reported by modifications within the `.submodules/` directory). In that case, just after the pull, you **have to run** `make up` to ensure consistency with regards the Git submodules:

Finally, you can upgrade the [Git submodules](.gitmodules) to the latest version by running:

    $> make upgrade

## Issues / Feature request

You can submit bug / issues / feature request using the [`ULHPC/ulhpc-docs` Project Tracker](https://gitlab.uni.lu/www/ulhpc-docs/issues)



## Advanced Topics

### Git

This repository make use of [Git](http://git-scm.com/) such that you should have it installed on your working machine: 

       $> apt-get install git-core # On Debian-like systems
       $> yum install git          # On CentOS-like systems
       $> brew install git         # On Mac OS, using [Homebrew](http://mxcl.github.com/homebrew/)
       $> port install git         # On Mac OS, using MacPort

Consider these resources to become more familiar (if not yet) with Git:

* [Simple Git Guide](http://rogerdudler.github.io/git-guide/)
* [Git book](http://book.git-scm.com/index.html)
* [Github:help](http://help.github.com/mac-set-up-git/)
* [Git reference](http://gitref.org/)

At least, you shall configure the following variables

       $> git config --global user.name "Your Name Comes Here"
       $> git config --global user.email you@yourdomain.example.com
       # configure colors
       $> git config --global color.diff auto
       $> git config --global color.status auto
       $> git config --global color.branch auto

Note that you can create git command aliases in `~/.gitconfig` as follows: 

       [alias]
           up = pull origin
           pu = push origin
           st = status
           df = diff
           ci = commit -s
           br = branch
           w  = whatchanged --abbrev-commit
           ls = ls-files
           gr = log --graph --oneline --decorate
           amend = commit --amend

Consider my personal [`.gitconfig`](https://github.com/Falkor/dotfiles/blob/master/git/.gitconfig) as an example -- if you decide to use it, simply copy it in your home directory and adapt the `[user]` section. 

### [Git-flow](https://github.com/petervanderdoes/gitflow-avh)

The Git branching model for this repository follows the guidelines of
[gitflow](http://nvie.com/posts/a-successful-git-branching-model/).
In particular, the central repository holds two main branches with an infinite lifetime:

* `production`: the *production-ready* branch
* `master`: the main branch where the latest developments interviene. This is the *default* branch you get when you clone the repository.

Thus you are more than encouraged to install the [git-flow](https://github.com/petervanderdoes/gitflow-avh) (AVH Edition, as the traditional one is no longer supported) extensions following the [installation procedures](https://github.com/petervanderdoes/gitflow-avh/wiki/Installation) to take full advantage of the proposed operations. The associated [bash completion](https://github.com/bobthecow/git-flow-completion) might interest you also.

### Releasing mechanism

The operation consisting of releasing a new version of this repository is automated by a set of tasks within the root `Makefile`.

In this context, a version number have the following format:

      <major>.<minor>.<patch>[-b<build>]

where:

* `< major >` corresponds to the major version number
* `< minor >` corresponds to the minor version number
* `< patch >` corresponds to the patching version number
* (eventually) `< build >` states the build number _i.e._ the total number of commits within the `master` branch.

Example: \`1.0.0-b28\`

The current version number is stored in the root file `VERSION`. __/!\ NEVER MAKE ANY MANUAL CHANGES TO THIS FILE__

For more information on the version, run:

     $> make versioninfo

If a new version number such be bumped, you simply have to run:

      $> make start_bump_{major,minor,patch}

This will start the release process for you using `git-flow`.
Once you have finished to commit your last changes, make the release effective by running:

      $> make release

It will finish the release using `git-flow`, create the appropriate tag in the `production` branch and merge all things the way they should be.

## Python Virtualenv / Pyenv and Direnv

You will have to ensure you have installed [direnv](https://direnv.net/) (configured by [`.envrc`](.envrc)), [pyenv](https://github.com/pyenv/pyenv) and [`pyenv-virtualenv`](https://github.com/pyenv/pyenv-virtualenv). This assumes also the presence of `~/.config/direnv/direnvrc` from [this page](https://github.com/Falkor/dotfiles/blob/master/direnv/direnvrc) - for more details, see [this blog post](https://varrette.gforge.uni.lu/blog/2019/09/10/using-pyenv-virtualenv-direnv/).

You can run the following command to setup your local machine in a compliant way:

```
make setup-pyenv   # AND/OR 'make setup-direnv'
```

Running `direnv allow` (this will have to be done only once), you should automatically enable the virtualenv `ulhpc-docs` based on the python version specified in [`.python-version`](.python-version). You'll eventually need to install the appropripriate Python version with `pyenv`:

```bash
pyenv versions   # Plural: show all versions
pyenv install $(head .python-version)
# Activate the virtualenv by reentering into the directory
cd ..
cd -
```

From that point, you should install the required packages using:

    pip install -r requirements.txt

Alternatively, you can use `make setup-python`

## Python Code Development

The Python code for `ulhpc-docs` is developed as a Python package, i.e. following the [official guidelines](https://packaging.python.org/overview/).

To play in live with the code while developing it, install it in "_editable_" mode by running:

    pip install -e ./

In practice:

    cd src
    make

Later on, you can clean the directory using

    make clean

Now you can enjoy live runs.
