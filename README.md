![By ULHPC](https://img.shields.io/badge/by-ULHPC-blue.svg) [![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](LICENSE) [![GitHub issues](https://img.shields.io/github/issues/ULHPC/ulhpc-docs)](https://github.com/ULHPC/ulhpc-docs/issues) [![Github](https://img.shields.io/badge/sources-github-green.svg)](https://github.com/ULHPC/ulhpc-docs/) ![Build Status](https://img.shields.io/github/workflow/status/ULHPC/ulhpc-docs/deploy) [![GitHub forks](https://img.shields.io/github/forks/ULHPC/ulhpc-docs?style=social)](https://github.com/ULHPC/ulhpc-docs) [![Github Stars](https://img.shields.io/github/stars/ULHPC/ulhpc-docs?style=social)](https://github.com/ULHPC/ulhpc-docs)

         _    _ _      _    _ _____   _____   _______        _           _           _   _____
        | |  | | |    | |  | |  __ \ / ____| |__   __|      | |         (_)         | | |  __ \
        | |  | | |    | |__| | |__) | |         | | ___  ___| |__  _ __  _  ___ __ _| | | |  | | ___   ___ ___
        | |  | | |    |  __  |  ___/| |         | |/ _ \/ __| '_ \| '_ \| |/ __/ _` | | | |  | |/ _ \ / __/ __|
        | |__| | |____| |  | | |    | |____     | |  __/ (__| | | | | | | | (__ (_| | | | |__| | (_) | (__\__ \
         \____/|______|_|  |_|_|     \_____|    |_|\___|\___|_| |_|_| |_|_|\___\__,_|_| |_____/ \___/ \___|___/


       Copyright (c) 2020-2022 S. Varrette and UL HPC Team <hpc-team@uni.lu>

This repository holds the [ULHPC Technical Documentation](https://hpc-docs.uni.lu), based on the [mkdocs-material](https://squidfunk.github.io/mkdocs-material/getting-started/) theme and the [PyMdown Extensions](https://facelessuser.github.io/pymdown-extensions/).
Inspired by the _excellent_ [NERSC Technical documentation](https://docs.nersc.gov/).


## Installation / Repository Setup

This repository is hosted on [Github](https://github.com/ULHPC/ulhpc-docs). To clone it, proceed as follows (adapt accordingly):

```bash
mkdir -p ~/git/github.com/ULHPC/
cd ~/git/github.com/ULHPC
git clone https://github.com/ULHPC/ulhpc-docs.git # or for SSH interactions: git clone git@github.com:ULHPC/ulhpc-docs.git
```

**`/!\ IMPORTANT`**: Once cloned, initiate your local copy of the repository by running:

```bash
$> cd ulhpc-docs
$> make setup
```

This will initiate the [Git submodules of this repository](.gitmodules) and setup the [git flow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) layout for this repository. It will also ensure python components ([direnv](https://direnv.net/), [pyenv](https://github.com/pyenv/pyenv) and [`pyenv-virtualenv`](https://github.com/pyenv/pyenv-virtualenv)) are installed.

Later on, you can update your local branches by running:

      make up

If upon pulling the repository, you end in a state where another collaborator have upgraded the Git submodules for this repository, you'll end in a dirty state (as reported by modifications within the `.submodules/` directory). In that case, just after the pull, you **have to run** `make up` to ensure consistency with regards the Git submodules:

Finally, you can upgrade the [Git submodules](.gitmodules) to the latest version by running:

      make upgrade


## Python Virtualenv / Pyenv and Direnv

You will have to ensure you have installed [direnv](https://direnv.net/), configured by [`.envrc`](.envrc)), [pyenv](https://github.com/pyenv/pyenv) and [`pyenv-virtualenv`](https://github.com/pyenv/pyenv-virtualenv). This assumes also the presence of `~/.config/direnv/direnvrc` from [this page](https://github.com/Falkor/dotfiles/blob/master/direnv/direnvrc) - for more details, see [this blog post](https://varrette.gforge.uni.lu/blog/2019/09/10/using-pyenv-virtualenv-direnv/).

```bash
### TL;DR; installation
# Mac OS
brew install direnv pyenv pyenv-virtualenv
# Linux/WSL
sudo { apt-get | yum | ... } install direnv
curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash
export PATH="$HOME/.pyenv/bin:$PATH"
pyenv root     # Should return $HOME/.pyenv
```

**Assuming** you have configured the [XDG Base Directories](https://specifications.freedesktop.org/basedir-spec/latest/) in your favorite shell configuration (`~/.bashrc`, `~/.zshrc` or `~/.profile`), you can enable direnv and pyenv as follows

```bash
# XDG  Base Directory Specification
# See https://specifications.freedesktop.org/basedir-spec/latest/
export XDG_CONFIG_HOME=$HOME/.config
export XDG_CACHE_HOME=$HOME/.cache
export XDG_DATA_HOME=$HOME/.local/share
# [...]
# Direnv - see https://direnv.net/
if [ -f "$HOME/.config/direnv/init.sh" ]; then
	. $HOME/.config/direnv/init.sh
fi
# - pyenv: https://github.com/pyenv/pyenv
# - pyenv-virtualenv: https://github.com/pyenv/pyenv-virtualenv
export PYENV_ROOT=$HOME/.pyenv
export PATH="${PYENV_ROOT}/bin:${PYENV_ROOT}/plugins/pyenv-virtualenv/bin:$PATH"
if [ -n "$(which pyenv)" ]; then
   eval "$(pyenv init -)"
   eval "$(pyenv virtualenv-init -)"
   export PYENV_VIRTUALENV_DISABLE_PROMPT=1
fi
```

Source your shell configuration file.
You can now run the following command to setup your local machine in a compliant way (this was normally done as part of the `make setup` step) :

```bash
# Global Direnv Setup (to be done only once)
make setup-direnv
make setup-pyenv
```


Running `direnv allow` (this will have to be done only once), you should automatically enable the virtualenv `ulhpc-docs` based on the python version specified in [`.python-version`](.python-version). You'll eventually need to install the appropriate Python version with `pyenv`:

```bash
pyenv versions   # Plural: show all versions
pyenv install $(head .python-version)
# Activate the virtualenv by reentering into the directory
direnv allow .
pyenv version # check current pyenv[-virtualenv] version. MUST return the vurtualenv 'ulhpc-docs'
```

From that point, you should install the required packages using:

``` bash
make setup-python

# OR (manually)
pip install --upgrade pip
pip install -r requirements.txt
```

# Documentation

See [`docs/`](docs/README.md).

The documentation for this project is handled by [`mkdocs`](http://www.mkdocs.org/#installation) with the [mkdocs-material](https://squidfunk.github.io/mkdocs-material/getting-started/) theme and the [PyMdown Extensions](https://facelessuser.github.io/pymdown-extensions/).
You might wish to generate locally the docs (**after** setting up your local virtualenv) i.e. to preview the documentation from the project root directory by running:

```bash
mkdocs serve    # OR make doc
```

Then visit with your favorite browser the URL `http://localhost:8000`. Alternatively, you can run `make doc` at the root of the repository.

## Reporting Issues / Feature request

You can submit bug / issues / feature request with our documentation using the [`ULHPC/ulhpc-docs` Issue Tracker](https://github.com/ULHPC/ulhpc-docs/issues).


## Software list

Several markdown files under `docs/software/swsets/` reflect the state of the software modules available on the ULHPC platform. They respect the following directory structure:

```
docs/software/swsets/
    ├── all_softwares.md   list of all software ever built
    ├── <version>.md       software list in RESIF swset <version>
    ├── <category>.md      list of all software belonging to category '<category>'
    └── <category>/
    .   ├── <software>.md    short summary and available version for software <software>
    .   └── [...]            belonging to category <category>
```

These files are **automatically** generated by the Python script [`scripts/resif3_module2markdown.py`](scripts/resif3_module2markdown.py):

```bash
$ ./scripts/resif3_module2markdown.py -h
Usage: resif3_module2markdown.py [OPTIONS] COMMAND [ARGS]...
[...]
Commands:
  collect  Collect meta-data dict of the RESIF3 modules installed and...
  render   Generate markdown files summarizing available ULHPC modules
```

* `./scripts/resif3_module2markdown.py collect [...]` is **expected to by run on one of the cluster** to access the RESIF root path `/opt/apps/resif`
     - use **`make resif-collect`** to perform the following operations:
          * upload the script and the necessary files on the cluster access frontend (see `RESIF_COLLECT_HOST` variable in [`.Makefile.local`](.Makefile.local))
          * generate a virtualenv under `RESIF_COLLECT_TMPDIR`
          * invoke the script in `collect` mode to generate the YAML file `RESIF_COLLECT_YAML`
          * download the generated yaml and store it under [`data/resif_modules.yaml`](data/resif_modules.yaml)
*  `./scripts/resif3_module2markdown.py render [...]` can be used locally to render/generate the markdown files **based on the data stored in [`data/resif_modules.yaml`](data/resif_modules.yam)**
    - use **`make resif-render`** to perform this action


## Contributors

See <https://github.com/ULHPC/ulhpc-docs/graphs/contributors>

You are more than welcome to contribute to the development of this project.
In order to get started, check out the [Contributing Guide](docs/contributing/README.md)

## License

Unless otherwise specified, this project and the sources proposed within this repository are released under the terms of the [CC BY-NC-SA 4.0](LICENSE) licence.
