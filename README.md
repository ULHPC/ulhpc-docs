[![By ULHPC](https://img.shields.io/badge/by-ULHPC-blue.svg)](https://hpc.uni.lu) [![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](LICENSE) [![GitHub issues](https://img.shields.io/github/issues/ULHPC/ulhpc-docs)](https://github.com/ULHPC/ulhpc-docs/issues) [![Github](https://img.shields.io/badge/sources-github-green.svg)](https://github.com/ULHPC/ulhpc-docs/) ![Build Status](https://img.shields.io/github/workflow/status/ULHPC/ulhpc-docs/deploy) [![GitHub forks](https://img.shields.io/github/forks/ULHPC/ulhpc-docs?style=social)](https://github.com/ULHPC/ulhpc-docs) [![Github Stars](https://img.shields.io/github/stars/ULHPC/ulhpc-docs?style=social)](https://github.com/ULHPC/ulhpc-docs) [![deploy](https://github.com/ULHPC/ulhpc-docs/actions/workflows/deploy.yml/badge.svg)](https://github.com/ULHPC/ulhpc-docs/actions/workflows/deploy.yml) [![pages-build-deployment](https://github.com/ULHPC/ulhpc-docs/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/ULHPC/ulhpc-docs/actions/workflows/pages/pages-build-deployment)

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
git clone https://github.com/ULHPC/ulhpc-docs.git # or for SSH interactions: git clone git@github.com:ULHPC/ulhpc-docs.git
```

To use the repository, you need to install some Python packages along with a compatible version of Python. If your system Python is compatible, simply install the packages in `requirements.txt`, ideally in a `venv`. For instance:
```
$ python3 -m venv "${HOME}/environments/ulhpc-docs"
$ source ~/environments/ulhpc-docs/bin/activate
$ pip install --upgrade pip
$ pip install --requirement requirements.txt
```

If your system Python is not compatible with the required packages, we suggest that you install Python in a Conda environment using the [Micromamba](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html) package manager for Conda.

- Begin by [installing the Micromamba package manager](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html).
- Install Python 3.8 in a new environment.
```
$ micromamba env create --name ulhpc-docs-python
$ micromamba install python=3.8 --channel conda-forge --name ulhpc-docs-python
```
- You now have 2 options. First options is to install the required python packages directly in the Conda environment.
```
$ micromamba activate ulhpc-docs-python
$ pip install --upgrade pip
$ pip install --requirement requirements.txt
```
- Alternatively, you can create a `venv` environment in which you install the packages.
```
$ micromamba run --name ulhpc-docs-python python -m venv "${HOME}/environments/ulhpc-docs"
$ source ~/environments/ulhpc-docs/bin/activate
$ pip install --upgrade pip
$ pip install --requirement requirements.txt
```

The `ulhpc-docs` `venv` environment will automatically use the Python installed in the Conda environment `ulhpc-docs-python`. In the later case you will no longer need to interact with the Conda environment, except perhaps for updating the Python executable.

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

The project was setup and populated by Sebastien Varrette, and received contributions from multiples persons -- see [`CONTRIBUTORS.md`](CONTRIBUTORS.md). 
To get up-to-date statistics, use

```bash 
make stats
````

In all cases, you are more than welcome to contribute to the development of this project.
In order to get started, check out the [Contributing Guide](docs/contributing/README.md)

## License

Unless otherwise specified, this project and the sources proposed within this repository are released under the terms of the [CC BY-NC-SA 4.0](LICENSE) licence.

[![](https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Cc-by-nc-sa_icon.svg/176px-Cc-by-nc-sa_icon.svg.png)](LICENSE)
