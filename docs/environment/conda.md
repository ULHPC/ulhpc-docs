# Self management of Conda work environments in UL HPC facilities

!!! important ""
    **TL;DR:** install and use the [Micromamba package manager](conda.md#the-micromamba-package-manager).

<!--intro-start-->

In some cases rare or rarely used packages are not available through the standard options such as [modules](modules.md). In such cases it may make sense to install the package locally with an environment manager such as Conda.

!!! warning "Contact the ULHPC before installing any software with Conda"
	Conda installs binaries that may not be optimal for the configuration of the ULHPC clusters. Prefer binaries provided through [modules](modules.md) or [containers](../../containers/), as these have been compiled with better optimized options for out clusters. Furthermore, installing packages locally with Conda consumes quotas in terms of [storage space and number of files](../../filesystems/quotas/#current-usage), in your or your project's account.
	
	Contact the ULHPC High Level Support Team in the [service portal](https://service.uni.lu/sp?id=index) [Home > Research > HPC > Software environment > Request expertise] to discuss possible options before installing any software.

[Conda](https://docs.conda.io/en/latest/) is an open source environment and package management system. With Conda you can create independent environments, where you can install applications such as python and R, together with any packages which will be used by these applications. The environments are independent with the Conda package manager resolving dependencies and ensuring that packages used in multiple environments are stored only once. In a typical setting, each user has their own installation of a Conda and a set of personal environments.

<!--intro-end-->

## A brief introduction to Conda

A few concepts are necessary to start working with Conda. In brief, these are package managers which are the programs used to create and manage environments, channels which are the repositories that contain the packages from which environments are composed, and distributions which are methods for shipping package managers.

### Package managers

Package managers are the programs that install and manage the Conda environments. There are multiple package managers, such as [`conda`](https://docs.conda.io/projects/conda/en/stable/), [`mamba`](https://mamba.readthedocs.io/en/latest/user_guide/mamba.html), and [`micromamba`](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html).

!!! important ""
    The UL HPC centre supports the use of [`micromamba`](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html) for the creation and management of personal Conda environments.

### Channels

Conda [channels](https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/channels.html#what-is-a-conda-channel) are the locations where packages are stored. There are also multiple channels, with some important channels being:

- [`defaults`](https://repo.anaconda.com/pkgs/), the default channel,
- [`anaconda`](https://anaconda.org/anaconda), a mirror of the default channel,
- [`bioconda`](https://anaconda.org/bioconda), a distribution of bioinformatics software, and
- [`conda-forge`](https://anaconda.org/conda-forge), a community-led collection of recipes, build infrastructure, and distributions for the conda package manager.

The most useful channel that comes pre-installed in all distributions, is Conda-Forge. Channels are usually hosted in the [official Anaconda page](https://anaconda.org/), but in some rare occasions [custom channels](https://conda.io/projects/conda/en/latest/user-guide/tasks/create-custom-channels.html) may be used. For instance the [default channel](https://repo.anaconda.com/pkgs/) is hosted independently from the official Anaconda page. Many channels also maintain web pages with documentation both for their usage and for packages they distribute:

- [Default Conda channel](https://docs.anaconda.com/free/anaconda/reference/default-repositories/)
- [Bioconda](https://bioconda.github.io/)
- [Conda-Forge](https://conda-forge.org/)

### Distributions

Quite often, the package manager is not distributed on its own, but with a set of packages that are required for the package manager to work, or even with some additional packages that required for most applications. For instance, the `conda` package manager is distributed with the Miniconda and Anaconda distributions. Miniconda contains the bare minimum packages for the `conda` package manager to work, and Anaconda contains multiple commonly used packages and a graphical user interface. The relation between these distributions and the package manager is depicted in the following diagram.

[![](images/Miniconda-vs-Anaconda.jpg)](images/Miniconda-vs-Anaconda.jpg)

The situation is similar in the [Mamba](https://mamba.readthedocs.io/en/latest/index.html) distributions. These distributions are supported by Conda-Forge, and by default they set-up `conda-forge` as the default and only channel during installation. The `defaults` or its mirror `anaconda` must be explicitly added if required. There is the [Mamba distribution](https://mamba.readthedocs.io/en/latest/user_guide/mamba.html) that comes with a minimal set of python packages required by the package manager, and the [Micromamba distribution](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html) that is distributed with no accompanying packages, as it is a standalone executable with no dependencies. Micromamba is using [`libmamba`](https://mamba.readthedocs.io/en/latest/index.html), a a C++ library implementing the Conda API.

## The Micromamba package manager

[![](https://mamba.readthedocs.io/en/latest/_static/logo.png){: style="width:200px; margin-right:10px; float: left;"}](https://mamba.readthedocs.io/en/latest/index.html)

The [Micromaba](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html) package manager is a minimal yet fairly complete implementation of the Conda interface in C++, that is shipped as a standalone executable. The package manager operates strictly on the user-space and thus it requires no special permissions are required to install packages. It maintains all its files in a couple of places, so uninstalling the package manager itself is also easy. Finally, the package manager is also lightweight and fast.

!!! important ""
    **UL HPC provides support only for the Micromamba package manager.**

### Installation

A complete guide regarding Micromamba installation can be found in the [official documentation](https://mamba.readthedocs.io/en/latest/micromamba-installation.html). To install micromamaba in the HPC clusters, log in to Aion or Iris. Working on a login node, run the installation script,
```bash
"${SHELL}" <(curl -L micro.mamba.pm/install.sh)
``` 
which will install the executable and setup the environment. There are 4 options to select during the installation of Micromamba:

- The directory for the installation of the binary file:
  ```
  Micromamba binary folder? [~/.local/bin]
  ```
  Leave empty and press enter to select the default displayed within brackets. Your `.bashrc` script should include `~/.local/bin` in the `$PATH` by default.
- The option to add to the environment autocomplete options for `micromamba`:
  ```
  Init shell (bash)? [Y/n]
  ```
  Press enter to select the default option `Y`. This will append a clearly marked section in the `.bashrc` shell. Do not forget to remove this section when uninstalling Micromamba.
- The option to configure the channels by adding conda-forge:
  ```
  Configure conda-forge? [Y/n]
  ```
  Press enter to select the default option `Y`. This will setup the `~/.condarc` file with `conda-forge` as the default channel. Note that Mamba and Micromamba will not use the `defaults` channel if it is not present in `~/.condarc` like `conda`.
- The option to select the directory where environment information and packages will be stored:
  ```
  Prefix location? [~/micromamba]
  ```
  Press enter to select the default option displayed within brackets.

To setup the environment log-out and log-in again. Now you can use `micromamba`, including the auto-completion feature.

### Managing environments

As an example, the creation and use of an environment for R jobs is presented. The command,
```bash
micromamba create --name R-project
```
creates an environment named `R-project`. The environment is activated with the command
```bash
micromamba activate R-project
```
anywhere in the file system.

Next, install the base R environment package that contains the R program, and any R packages required by the project. To install packages, first ensure that the `R-project` environment is active, and then install any package with the command
```bash
micromamba install <package_name>
```
all the required packages. Quite often, the channel name must also be specified:
```bash
micromamba install --chanell <chanell_name> <package_name>
```
Packages can be found by searching the [conda-forge channel](https://anaconda.org/conda-forge).

For instance, the basic functionality of the R software environment is contained in the `r-base` package. Calling
```bash
micromamba install --channel conda-forge r-base
```
will install all the components required to run standalone R scripts. More involved scripts use functionality defined in various packages. The R packages are prepended with a prefix 'r-'. Thus, `plm` becomes `r-plm` and so on. After all the required packages have been installed, the environment is ready for use.

Packages in the conda-forge channel come with instructions for their installation. Quite often the channel is specified in the installation instructions, `-c conda-forge` or `--channel conda-forge`. While the Micromamba installer sets-up `conda-forge` as the default channel, latter modification in `~/.condarc` may change the channel priority. Thus it is a good practice to explicitly specify the source channel when installing a package.

After work in an environment is complete, deactivate the environment,
```bash
micromamba deactivate
```
to ensure that it does not interfere with any other operations. In contrast to [modules](modules.md), Conda is designed to operate with a single environment active at a time. Create one environment for each project, and Conda will ensure that any package that is shared between multiple environments is installed once.

Micromamba supports almost all the subcommands of Conda. For more details see the [official documentation](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html).

### Using environments in submission scripts

Since all computationally heavy operations must be performed in compute nodes, Conda environments are also used in jobs submitted to the [queuing system](../slurm/index.md). Returning to the R example, a submission script running a single core R job can use the `R-project_name` environment as follows:
```
#SBATCH --job-name R-test-job
#SBATCH --nodes 1
#SBATCH --ntasks-per-node 1
#SBATCH --cpus-per-task 1
#SBATCH --time=0-02:00:00
#SBATCH --partition batch
#SBATCH --qos normal

echo "Launched at $(date)"
echo "Job ID: ${SLURM_JOBID}"
echo "Node list: ${SLURM_NODELIST}"
echo "Submit dir.: ${SLURM_SUBMIT_DIR}"
echo "Numb. of cores: ${SLURM_CPUS_PER_TASK}"

micromamba activate R-project

export SRUN_CPUS_PER_TASK="${SLURM_CPUS_PER_TASK}"
export OMP_NUM_THREADS=1
srun Rscript --no-save --no-restore script.R

micromamba deactivate
```

_Useful scripting resources_

- [Formatting submission scripts for R (and other systems)](../slurm/launchers.md#serial-task-script-launcher)

## Combining Conda with other package and environment management tools

It may be desirable to use Conda to manage environments but a different tool to manage packages, such as [`pip`](https://pip.pypa.io/en/stable/getting-started/). Or subenvironments may need to be used inside a Conda environment, as for instance with tools for creating and managing isolated Python installation, such as [`virtualenv`](https://virtualenv.pypa.io/en/latest/), or with tools for integrating managed Python installations and packages in project directories, such as [Pipenv](https://pipenv.pypa.io/en/latest) and [Poetry](https://python-poetry.org/).

Conda integrates well with any such tool. Some of the most frequent cases are described bellow.

### Managing packages with external tools

Quite often a package that is required in an environment is not available through a Conda channel, but it is available through some other distribution channel, such as the [Python Package Index (PyPI)](https://pypi.org/). In these cases the only solution is to create a Conda environment and install the required packages with `pip` from the Python Package Index.

Using an external packaging tool is possible because of the method that Conda uses to install packages. Conda installs package versions in a central directory (e.g. `~/micromamba/pkgs`). Any environment that requires a package links to the central directory with _hard links_. Links are added to the home directory (e.g. `~/micromamba/envs/R-project` for the `R-project` environment) of any environment that requires them. When using an external package tool, package components are installed in the same directory where Conda would install the corresponding link. Thus, external package management tools integrate seamlessly with Conda, with a couple of caveats:

- each package must be managed by one tool, otherwise package components will get overwritten, and
- packages installed by the package tool are specific to an environment and cannot be shared as with Conda, since components are installed directly and not with links.

!!! important "Prefer Conda over external package managers"
    Installing the same package in multiple environments with an external package tool consumes quotas in terms of [storage space and number of files](../../filesystems/quotas/#current-usage), so prefer Conda when possible. This is particularly important for the `inode` limit, since some packages install a large number of files, and the hard links used by Conda do not consume inodes or [disk space](https://saturncloud.io/blog/understanding-conda-clean-where-does-it-remove-packages-from/).

#### Pip

In this example `pip` is used to manage packages in a Conda environment with [MkDocs](https://www.mkdocs.org/) related packages. To install the packages, create an environment
```bash
micromamba env create --name mkdocs
```
activate the environment,
```bash
micromamba activate mkdocs
```
and install `pip`
```bash
micromamba install --channel conda-forge pip
```
which will be used to install the remaining packages.

The `pip` will be the only package that will be managed with Conda. For instance, to update Pip activate the environment,
```bash
micromamba activate mkdocs
```
and run
```bash
micromaba update --all
```
to update all installed packaged (only `pip` in our case). All other packages are managed by `pip`.

For instance, assume that a `mkdocs` project requires the following packages:

- `mkdocs`
- `mkdocs-minify-plugin`

The package `mkdocs-minify-plugin` is less popular and thus is is not available though a Conda channel, but it is available in PyPI. To install it, activate the `mkdocs` environment
```bash
micromamba activate mkdocs
```
and install the required packages with `pip`
```bash
pip install --upgrade mkdocs mkdocs-minify-plugin
```
inside the environment. The packages will be installed inside a directory that `micromamba` created for the Conda environment, for instance
```
${HOME}/micromamba/envs/mkdocs
```
along side packages installed by `micromamba`. As a results, 'system-wide' installations with `pip` inside a Conda environment do not interfere with system packages.

!!! warning "Do not install packages in Conda environments with pip as a user"
    User installed packages (e.g.`pip install --user --upgrade mkdocs-minify-plugin`) are installed in the same directory for all environments, typically in `~/.local/`, and can interfere with other versions of the same package installed from other Conda environments.

### Combining Conda with external environment management tools

Quite often it is required to create isolated environments using external tools. For instance, tools such as [`virtualenv`](https://virtualenv.pypa.io/en/latest/) can install and manage a Python distribution in a given directory and export and import environment descriptions from text files. This functionalities allows for instance the shipping of a description the Python environment as part of a project. Higher level tools such as [`pipenv`](https://pipenv.pypa.io/en/latest) automate the process of managing Python project environments whereas [`poetry`](https://python-poetry.org/) is a wholistic project management tool with integrated management of Python environments.

Installing and using in Conda environments tools that create isolated environments is relatively straight forward. Create an environment where only the required that tool is installed, and manage any project subenvironments using the installed tool.

!!! important "Create a different environment for each tool"
    While this is not a requirement it is a good practice. For instance, `pipenv` and `poetry` used to and may still have conflicting dependencies; Conda detects the dependency and aborts the conflicting installation.

#### Pipenv

To demonstrate the usage of `pipenv`, create a Conda environment,
```bash
micromamba enc create --name pipenv
```
activate it
```bash
micromamba activate pipenv
```
and install the `pipenv` package
```bash
micromamba install --channel conda-forge pipenv
```
 as the only package in this environment. Now the `pipenv` is managed with Conda, for instance to update `pipenv` activate the environment
```bash
micromamba activate pipenv
```
and call
```bash
micromamba update --all
```
to update the single installed package. Inside the environment use `pipenv` as usual to create and manage project environments.
