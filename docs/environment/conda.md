# Self management of Conda work environments in UL HPC facilities

!!! important ""
    **TL;DR:** [install and use the Micromamba package manager](#The Micromamba package manager).

<!--intro-start-->

[Conda](https://docs.conda.io/en/latest/) is an open source environment and package management system. With Conda you can create independent environments, where you can install applications such as python and R, together with any packages which will be used by these applications. The environments are independent with the Conda package manager resolving dependencies and ensuring that packages used in multiple environments are stored only once. In a typical setting, each user has their own installation of a Conda and a set of personal environments.

<!--intro-end-->

## A brief introduction to Conda

A few concepts are necessary to start working with Conda. In brief these are package managers which are the programs used to handle the environment, channels which are the repositories that contain the packages from which environments are composed, and distributions which are methods for shipping package managers.

### Package managers

Package managers are the programms that install and manage the Conda environments. There are multiple package managers, such as [`conda`](https://docs.conda.io/projects/conda/en/stable/), [`mamba`](https://mamba.readthedocs.io/en/latest/user_guide/mamba.html), and [`micromamba`](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html).

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

The [Micromaba](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html) package manager is a minimal but complete implementation of the Conda interface in C++, that is shipped as a standalone executable. The package manager operates strictly on the user-space and thus it requires no special permissions are required to install packages. It maintains all its files in a couple of places, so uninstalling the package manager itself is also easy. Finally, the package manager is also lightweight and fast.

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
micromamba create --name R-project_name
```
creates an environment named `R-project_name`. The environment is activated with the command:
```bash
micromamba activate R-project_name
```
The environment is deactivated with the command:
```bash
micromamba deactivate
```

The next step is the installation of the base R environment that contains the R program, and any R packages required by the project. To install packages the environment is first activated with `micromamba activate R-project_name`, and then packages are installed with the command:
```bash
micromamba install <package_name>
```
Quite often, the channel name must also be specified:
```bash
micromamba install --chanell <chanell_name> <package_name>
```

Packages can be searched in the [conda-forge channel](https://anaconda.org/conda-forge). For instance, to install R:
```bash
micromamba install --channel conda-forge r-base
```
The R packages are prepended with a prefix 'r-'. Thus, `plm` becomes `r-plm` and so on. Packages in the conda-forge channel come with instructions for their installation. Quite often the channel is specified in the installation instructions, `-c conda-forge` or `--channel conda-forge`. While the Micromamba installer sets-up `conda-forge` as the default channel, latter modification in `~/.condarc` may change the channel priority. Thus it is a good practice to explicitly specify the source channel when installing a package.

After all the required packages have been installed, work in the environment can continue, or the environment can be deactivated and used later. Micromamba supports almost all the subcommands of Conda. For more details see the [official documentation](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html).

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

micromamba activate R-project_name

export SRUN_CPUS_PER_TASK="${SLURM_CPUS_PER_TASK}"
export OMP_NUM_THREADS=1
srun Rscript --no-save --no-restore script.R

micromamba deactivate
```

_Useful scripting resources_

- [Formatting submission scripts for R (and other systems)](../slurm/launchers.md#serial-task-script-launcher)

## Combining Conda with package and environment management tools

Quite often it may be desirable to use Conda to manage environments but a different tool to manage packages. For instance we may want to install some packages that are not available in a Conda channel with Pip. We may also want to manage sub-environments with a different tool. For instance we may want to setup some project in a directory with Pipenv. Conda integrates well with any such tool given that each package is managed by a unique tool. Some of the most frequent cases are described bellow.

### Managing packages with different tools

#### Pip

Many less popular Python packages are available through Pip but they are not found in any Conda channel. For instance, to manage an environment with `mkdocs` packages from Pip, create and environment
```bash
micromamba env create --name mkdocs
```
activate the environment,
```bash
micromamba activate mkdocs
```
and install `pip`:
```bash
micromamba install --channel conda-forge pip
```

The `pip` will be the only package that will be managed with Conda. For instance, to update Pip activate the environment,
```bash
micromamba activate mkdocs
```
and run:
```bash
micromaba update --all
```
All other packages are now managed by `pip`.

For instance, assume that a `mkdocs` project requires the following packages:
- `mkdocs`
- `mkdocs-minify-plugin`
The package `mkdocs-minify-plugin` is not available in Conda, but is available with Pip. To install it, activate the `mkdocs` environment
```bash
micromamba activate mkdocs
```
and install the required packages with `pip`:
```bash
pip install mkdocs mkdocs-minify-plugin
```
The packages will be installed inside the micromamba directory, for instance
```
${HOME}/micromamba/envs/mkdocs
```
and will not interfere with system packages.

!!! important ""
    **Do not install packages with pip as a user:** User packages are installed in the same directory for all environments, and can interfere with other versions of the same package.

### Combining Conda with other environment and package management tools

Quite often the user may want to create subenvironments, for instance tools such as `pipenv` and `poetry` manage environment and packages as project files, which an be stored in a project directory and version controlled as part of a project. Using such tools with Conda is relatively straight forward. Create an environment where only the tool that you require is installed, and manage the project subenvironments using the installed tool.

!!! important ""
    **Create a different environment for each tool:** While this is not a requirement it is a good practice. For instance, `pipenv` and `poetry` used to and may still have conflicting dependencies.

#### Pipenv

To demonstrate the usage of `pipenv`, create a Conda environment,
```bash
micromamba enc create --name pipenv
```
activate it
```bash
micromamba activate pipenv
```
and install the `pipenv` package as the only package in this environment:
```bash
micromamba install --channel conda-forge pipenv
```
Now the `pipenv` is managed with Conda, for instance to update `pipenv` activate the environment
```bash
micromamba activate pipenv
```
and call:
```bash
micromamba update --all
```
Inside the environment use `pipenv` as usual to create and manage project environments.
