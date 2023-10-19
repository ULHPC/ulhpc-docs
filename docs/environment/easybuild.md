# Easybuild

<!--intro-start-->

[![](https://easybuild.readthedocs.io/en/latest/_static/easybuild_logo_alpha.png){:style="width:200px; float: right;"}](https://easybuild.readthedocs.io/)

[EasyBuild](https://docs.easybuild.io/) (EB for short) is a software build and installation framework that allows you to manage (scientific) software on High Performance Computing (HPC) systems in an efficient way.
A large number of scientific software are supported (**at least [2175 supported software packages](https://docs.easybuild.io/en/latest/version-specific/Supported_software.html)** since the 4.3.2 release) - see also [What is EasyBuild?](https://docs.easybuild.io/en/latest/Introduction.html).

For several years now, [Easybuild](https://docs.easybuild.io/) is used to [manage the ULHPC User Software Set](modules.md#ulhpc-toolchains-and-software-set-versioning) and generate automatically the module files available to you on our computational resources in either `prod` (default) or `devel` (early development/testing) environment -- see [ULHPC Toolchains and Software Set Versioning](../environment/modules.md#ulhpc-toolchains-and-software-set-versioning).
This enables users to easily _extend_ the global [Software Set](modules.md#ulhpc-toolchains-and-software-set-versioning) with their own **local** software
builds, either performed within their [global home
directory](../data/layout.md#global-home-directory-home) or (_better_) in a shared [project
directory](../data/layout.md) though [Easybuild](../environment/easybuild.md), which generate automatically module files compliant with the [ULHPC module setup](../environment/modules.md).

<!--intro-end-->

??? question "Why using an automatic building tool on HPC environment like [Easybuild](https://docs.easybuild.io) or [Spack](https://spack.io/)?"
    Well that may seem obvious to some of you, but scientific software is often **difficult** to build.
    Not all rely on _standard_ building tools like Autotools/Automake (and the famous `configure; make; make install`) or CMake.
    And even in that case, parsing the available option to ensure matching the hardware configuration of the computing resources used for the execution is time consuming and error-prone.
    Most of the time unfortunately, scientific software embed hardcoded parameters and/or poor/outdated documentation with incomplete build procedures.

    In this context,  software build and installation frameworks like [Easybuild](https://docs.easybuild.io) or [Spack](https://spack.io/) helps to facilitate the building task in a _consistent_ and _automatic_ way, while generating also the LMod modulefiles.

    We select [Easybuild](https://docs.easybuild.io) as primary building tool to ensure the best optimized builds.
    Some HPC sites use both -- see [this talk from William Lucas at EPCC](https://www.archer2.ac.uk/training/courses/200617-spack-easybuild/) for instance.

    It does not prevent from maintaining your own [build instructions notes](https://github.com/hpc-uk/build-instructions).

## Easybuild Concepts and terminology

[:fontawesome-solid-sign-in-alt: Official Easybuild Tutorial](https://easybuilders.github.io/easybuild-tutorial/){: .md-button .md-button--link}

EasyBuild relies on two main concepts: *[Toolchains](https://docs.easybuild.io/en/latest/Concepts_and_Terminology.html#toolchains)* and *[EasyConfig files](https://docs.easybuild.io/en/latest/Concepts_and_Terminology.html#easyconfig-files)*.

A **toolchain** corresponds to a compiler and a set of libraries which are commonly used to build a software.
The two main toolchains frequently used on the UL HPC platform are the `foss` ("_Free and Open Source Software_") and the `intel` one.

1. `foss`, based on the GCC compiler and on open-source libraries (OpenMPI, OpenBLAS, etc.).
2. `intel`, based on the Intel compiler suit ([])and on Intel libraries (Intel MPI, Intel Math Kernel Library, etc.).

An **[EasyConfig file](http://easybuild.readthedocs.io/en/latest/Writing_easyconfig_files.html)** is a simple text file that describes the build process of a software. For most software that uses standard procedures (like `configure`, `make` and `make install`), this file is very simple.
Many [EasyConfig files](https://github.com/easybuilders/easybuild-easyconfigs/tree/master/easybuild/easyconfigs) are already provided with EasyBuild.


## ULHPC Easybuild Configuration

To build software with [Easybuild](https://docs.easybuild.io/) compliant with the configuration in place on the ULHPC facility, you need to be aware of the following setup:

* [Modules](modules.md) tool (`$EASYBUILD_MODULES_TOOL`): [Lmod](http://lmod.readthedocs.io/) (see [docs](https://docs.easybuild.io/en/latest/Configuration.html#prefix))
* [Module Naming Scheme](modules.md#module-naming-schemes) (`EASYBUILD_MODULE_NAMING_SCHEME`): we use a special **hierarchical** organization where the software are classified/**categorized** under a pre-defined class.

These variables are defined at the global profile level, under `/etc/profile.d/ulhpc_resif.sh` on the compute nodes as follows:

```bash
export EASYBUILD_MODULES_TOOL=Lmod
export EASYBUILD_MODULE_NAMING_SCHEME=CategorizedModuleNamingScheme
```

All builds and installations are performed at user level, so you don't need the admin (i.e. `root`) rights.
Another **very** important configuration variable is the Overall [Easybuild prefix path](https://docs.easybuild.io/en/latest/Configuration.html#prefix) `$EASYBUILD_PREFIX` which affects the _default_ value of several configuration options:

* built software are placed under `${EASYBUILD_PREFIX}/software/`
* modules install path: `${EASYBUILD_PREFIX}/modules/all` (determined via Overall prefix path (--prefix), --subdir-modules and --suffix-modules-path)

You can thus extend the [ULHPC Software set](modules.md#ulhpc-toolchains-and-software-set-versioning) with your own local builds by setting appropriately the variable `$EASYBUILD_PREFIX`:

* For installation in your home directory: `export EASYBUILD_PREFIX=$HOME/.local/easybuild`
* For installation in a [shared project directory](../data/project.md) `<name>`: `export EASYBUILD_PREFIX=$PROJECTHOME/<name>/easybuild`

!!! tips "Adapting you custom build to cluster, the toolchain version and the architecture"
    Just like the ULHPC software set ([installed in
    `EASYBUILD_PREFIX=/opt/apps/resif/<cluster>/<version>/<arch>`](modules.md#ulhpc-modulepath)),
    you may want to isolate your local builds to take into account
    the cluster `$ULHPC_CLUSTER` ("iris" or "aion"), the
    toolchain version `<version>` (Ex: 2019b, 2020b etc.) you build upon and
    eventually the architecture `<arch>`.
    In that case, you can use the following helper scripts:
    ```bash
    resif-load-home-swset-prod
    ```
    which is roughly equivalent to the following code:
    ```bash
    # EASYBUILD_PREFIX: [basedir]/<cluster>/<environment>/<arch>
    # Ex: Default EASYBUILD_PREFIX in your home - Adapt to project directory if needed
    _EB_PREFIX=$HOME/.local/easybuild
    # ... eventually complemented with cluster
    [ -n "${ULHPC_CLUSTER}" ] && _EB_PREFIX="${_EB_PREFIX}/${ULHPC_CLUSTER}"
    # ... eventually complemented with software set version
    _EB_PREFIX="${_EB_PREFIX}/${RESIF_VERSION_PROD}"
    # ... eventually complemented with arch
    [ -n "${RESIF_ARCH}" ] && _EB_PREFIX="${_EB_PREFIX}/${RESIF_ARCH}"
    export EASYBUILD_PREFIX="${_EB_PREFIX}"
    export LOCAL_MODULES=${EASYBUILD_PREFIX}/modules/all
    ```

    For a shared project directory `<name>` located under `$PROJECTHOME/<name>`, you can use the following following helper scripts:
    ```bash
    resif-load-project-swset-prod $PROJECTHOME/<name>
    ```

!!! important "ACM PEARC'21: RESIF 3.0"
    For more details on the way we setup and deploy the User Software Environment on ULHPC systems through the RESIF 3 framework, see the [ACM PEARC'21](https://hpc.uni.lu/blog/2021-05-11-resif-3) conference paper presented on July 22, 2021.
    > __ACM Reference Format__ | [ORBilu entry](https://orbilu.uni.lu/handle/10993/47115) | [OpenAccess](https://dl.acm.org/doi/10.1145/3437359.3465600) | [ULHPC blog post](https://hpc.uni.lu/blog/2021-05-11-resif-3) | [slides](https://hpc.uni.lu/download/slides/2021-07-22-ACM-PEARC21_resif3.pdf) | [Github](https://github.com/ULHPC/sw): <br/>
    > Sebastien Varrette, Emmanuel Kieffer, Frederic Pinel, Ezhilmathi Krishnasamy, Sarah Peter, Hyacinthe Cartiaux, and Xavier Besseron. 2021. RESIF 3.0: Toward a Flexible & Automated Management of User Software Environment on HPC facility. _In Practice and Experience in Advanced Research Computing (PEARC '21)_. Association for Computing Machinery (ACM), New York, NY, USA, Article 33, 1–4. https://doi.org/10.1145/3437359.3465600

## Installation / Update local Easybuild

You can of course use the _default_ Easubuild that comes with the ULHPC software
setwith `module load tools/EasyBuild`.
But as soon as you want to install your local builds, you have interest to
install the up-to-date release of [EasyBuild](https://docs.easybuild.io/) in
your local `$EASYBUILD_PREFIX`.
You can later update any time [EasyBuild](https://docs.easybuild.io/) in
`$EASYBUILD_PREFIX` via the same [bootstrapping procedure](https://docs.easybuild.io/en/latest/Installation.html#bootstrapping-easybuild):

```bash
### /!\ IMPORTANT: You need to be on a computing node to access the module
###                command and permit the installation
# download script
curl -o /tmp/bootstrap_eb.py https://raw.githubusercontent.com/easybuilders/easybuild-framework/develop/easybuild/scripts/bootstrap_eb.py
# double check the installation prefix
echo $EASYBUILD_PREFIX
# install Easybuild
python /tmp/bootstrap_eb.py $EASYBUILD_PREFIX
```

Repeat when you need to update your local installation.
