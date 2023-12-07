# Environment Setup

AWS suggest to use Spack to setup your software environment. There is no hard requirement that you must use Spack. However we have included it here, as it is a quick, simple way to setup a development environment.
The official ULHPC swsets are not available on the AWS cluster. If you prefer to use [EasyBuild](../environment/easybuild) or manually compile softwares, please refer to the [ULHPC software documentation](../software/build) for this purpose.


## Environment modules and LMod ##

Like the ULHPC facility, the AWS cluster  relies on the [Environment Modules](http://modules.sourceforge.net/) / [LMod](http://lmod.readthedocs.io/en/latest/) framework which provided the [`module`](http://lmod.readthedocs.io) utility **on Compute nodes**
to manage nearly all software.
There are two main advantages of the `module` approach:

1. ULHPC can provide many different versions and/or installations of a
   single software package on a given machine, including a default
   version as well as several older and newer version.
2. Users can easily switch to different versions or installations
   without having to explicitly specify different paths. With modules,
   the `PATH` and related environment variables (`LD_LIBRARY_PATH`, `MANPATH`, etc.) are automatically managed.

[Environment Modules](http://modules.sourceforge.net/) in itself are a standard and well-established technology across HPC sites, to permit developing and using complex software and libraries build with dependencies, allowing multiple versions of software stacks and combinations thereof to co-exist.
It **brings the `module` command** which is used to manage environment variables such as `PATH`, `LD_LIBRARY_PATH` and `MANPATH`, enabling the easy loading and unloading of application/library profiles and their dependencies.

See <https://hpc-docs.uni.lu/environment/modules/> for more details


| Command                        | Description                                                   |
|--------------------------------|---------------------------------------------------------------|
| `module avail`                 | Lists all the modules which are available to be loaded        |
| `module spider <pattern>`      | Search for <pattern> among available modules **(Lmod only)**  |
| `module load <mod1> [mod2...]` | Load a module                                                 |
| `module unload <module>`       | Unload a module                                               |
| `module list`                  | List loaded modules                                           |
| `module purge`                 | Unload all modules (purge)                                    |
| `module display <module>`      | Display what a module does                                    |
| `module use <path>`            | Prepend the directory to the MODULEPATH environment variable  |
| `module unuse <path>`          | Remove the directory from the MODULEPATH environment variable |

At the heart of environment modules interaction resides the following components:

* the `MODULEPATH` environment variable, which defines the list of searched directories for modulefiles
* `modulefile`

Take a look at the current values:

```bash
$ echo $MODULEPATH
/shared/apps/easybuild/modules/all:/usr/share/Modules/modulefiles:/etc/modulefiles:/usr/share/modulefiles/Linux:/usr/share/modulefiles/Core:/usr/share/lmod/lmod/modulefiles/Core
$ module show toolchain/foss
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
   /shared/apps/easybuild/modules/all/toolchain/foss/2022b.lua:
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
help([[
Description
===========
GNU Compiler Collection (GCC) based compiler toolchain, including
 OpenMPI for MPI support, OpenBLAS (BLAS and LAPACK support), FFTW and ScaLAPACK.


More information
================
 - Homepage: https://easybuild.readthedocs.io/en/master/Common-toolchains.html#foss-toolchain
]])
whatis("Description: GNU Compiler Collection (GCC) based compiler toolchain, including
 OpenMPI for MPI support, OpenBLAS (BLAS and LAPACK support), FFTW and ScaLAPACK.")
whatis("Homepage: https://easybuild.readthedocs.io/en/master/Common-toolchains.html#foss-toolchain")
whatis("URL: https://easybuild.readthedocs.io/en/master/Common-toolchains.html#foss-toolchain")
conflict("toolchain/foss")
load("compiler/GCC/12.2.0")
load("mpi/OpenMPI/4.1.4-GCC-12.2.0")
load("lib/FlexiBLAS/3.2.1-GCC-12.2.0")
load("numlib/FFTW/3.3.10-GCC-12.2.0")
load("numlib/FFTW.MPI/3.3.10-gompi-2022b")
load("numlib/ScaLAPACK/2.2.0-gompi-2022b-fb")
setenv("EBROOTFOSS","/shared/apps/easybuild/software/foss/2022b")
setenv("EBVERSIONFOSS","2022b")
setenv("EBDEVELFOSS","/shared/apps/easybuild/software/foss/2022b/easybuild/toolchain-foss-2022b-easybuild-devel")
```
Now you can search for a given software using `module spider <pattern>`:

```bash
$  module spider lang/Python
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  lang/Python:
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Description:
      Python is a programming language that lets you work more quickly and integrate your systems more effectively.

     Versions:
        lang/Python/3.10.8-GCCcore-12.2.0-bare
        lang/Python/3.10.8-GCCcore-12.2.0

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  For detailed information about a specific "lang/Python" module (including how to load the modules) use the module's full name.
  For example:

     $ module spider lang/Python/3.10.8-GCCcore-12.2.0
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```

Let's see the effect of loading/unloading a module

```bash
$ module list
No modules loaded
$ which python
/usr/bin/python
$ python --version       # System level python
Python 2.7.18

$ module load lang/Python    # use TAB to auto-complete
$ which python
/shared/apps/easybuild/software/Python/3.10.8-GCCcore-12.2.0/bin/python
$ python --version
Python 3.10.8
$ module purge
```

## Installing softwares with [Easybuild](https://easybuild.io/)

[<img width='150px' src='https://easybuild.io/images/easybuild_logo_horizontal.png'/>](https://easybuilders.github.io/easybuild/)

EasyBuild is a tool that allows to perform automated and reproducible compilation and installation of software. A large number of scientific software are supported (**[2995 supported software packages](http://easybuild.readthedocs.io/en/latest/version-specific/Supported_software.html)** in the last release 4.8.0) -- see also [What is EasyBuild?](http://easybuild.readthedocs.io/en/latest/Introduction.html)

All builds and installations are performed at user level, so you don't need the admin (i.e. `root`) rights.
The software are installed in your home directory under `$EASYBUILD_PREFIX` -- see <https://hpc-docs.uni.lu/environment/easybuild/>

|                     | Default setting (local)  | Recommended setting       |
|---------------------|--------------------------|---------------------------|
| `$EASYBUILD_PREFIX` | `$HOME/.local/easybuild` | `/shared/apps/easybuild/` |
|                     |                          |                           |

* built software are placed under `${EASYBUILD_PREFIX}/software/`
* modules install path `${EASYBUILD_PREFIX}/modules/all`


### Easybuild main concepts

See also the [official Easybuild Tutorial: "Maintaining a Modern Scientific Software Stack Made Easy with EasyBuild"](https://easybuilders.github.io/easybuild-tutorial/2021-isc21/)

EasyBuild relies on two main concepts: *Toolchains* and *EasyConfig files*.

A **toolchain** corresponds to a compiler and a set of libraries which are commonly used to build a software.
The two main toolchains frequently used on the UL HPC platform are the `foss` ("_Free and Open Source Software_") and the `intel` one.

1. `foss`  is based on the GCC compiler and on open-source libraries (OpenMPI, OpenBLAS, etc.).
2. `intel` is based on the Intel compiler and on Intel libraries (Intel MPI, Intel Math Kernel Library, etc.).

An **EasyConfig file** is a simple text file that describes the build process of a software. For most software that uses standard procedures (like `configure`, `make` and `make install`), this file is very simple.
Many [EasyConfig files](https://github.com/easybuilders/easybuild-easyconfigs/tree/master/easybuild/easyconfigs) are already provided with EasyBuild.
By default, EasyConfig files and generated modules are named using the following convention:
`<Software-Name>-<Software-Version>-<Toolchain-Name>-<Toolchain-Version>`.
However, we use a **hierarchical** approach where the software are classified under a category (or class) -- see  the `CategorizedModuleNamingScheme` option for the `EASYBUILD_MODULE_NAMING_SCHEME` environmental variable), meaning that the layout will respect the following hierarchy:
`<Software-Class>/<Software-Name>/<Software-Version>-<Toolchain-Name>-<Toolchain-Version>`

Additional details are available on EasyBuild website:

- [EasyBuild homepage](https://easybuilders.github.io/easybuild/)
- [EasyBuild documentation](http://easybuild.readthedocs.io/)
- [What is EasyBuild?](http://easybuild.readthedocs.io/en/latest/Introduction.html)
- [Toolchains](https://github.com/easybuilders/easybuild/wiki/Compiler-toolchains)
- [EasyConfig files](http://easybuild.readthedocs.io/en/latest/Writing_easyconfig_files.html)
- [List of supported software packages](http://easybuild.readthedocs.io/en/latest/version-specific/Supported_software.html)

Easybuild is provided to you as a software module to complement the existing software set. 

``` bash
module load tools/EasyBuild
```

In case you cant to install the latest version yourself, please follow [the official instructions](http://easybuild.readthedocs.io/en/latest/Installation.html).
Nonetheless, we strongly recommand to use the provided module.
**Don't forget** to setup your local Easybuild configuration first.

What is important for the installation of Easybuild are the following variables:

* `EASYBUILD_PREFIX`: where to install **local** modules and software, _i.e._ `$HOME/.local/easybuild`
* `EASYBUILD_MODULES_TOOL`: the type of [modules](http://modules.sourceforge.net/) tool you are using, _i.e._ `LMod` in this case
* `EASYBUILD_MODULE_NAMING_SCHEME`: the way the software and modules should be organized (flat view or hierarchical) -- we're advising on `CategorizedModuleNamingScheme`

!!! danger "Important"
    * Recall that **you should be on a compute node to install [Easybuild](http://easybuild.readthedocs.io)** (otherwise the checks of the `module` command availability will fail.)

### Install a missing software by complementing the software set

The current software set contains the toolchain [foss-2022b](https://docs.easybuild.io/common-toolchains/#common_toolchains_update_cycle) that is necessary to build other softwares. We have build OpenMPI-4.1.4 to take in account the latest AWS EFA and the slurm integration.
In order to install missing softwares for your project, you can complement the existing software set located at `/shared/apps/easybuild` by using the provided EasyBuild module (latest version).   
Once Easybuild has been loaded, you can search and install new softwares. By default, these new softwares will be installed at `${HOME}/.local/easybuild`. Feel free to adapt the environment variable `${EASYBUILD_PREFIX}` to select a new installation directory. 

Let's try to install a missing software

``` bash
(heanode)$ srun -p small -N 1 -n1 -c16  --pty bash -i
(node)$ module spider HPL   # HPL is a software package that solves a (random) dense linear system in double precision (64 bits)
Lmod has detected the following error:  Unable to find: "HPL".
(node)$ module load tools/EasyBuild
# Search for recipes for the missing software
(node)$ eb -S HPL
== found valid index for /shared/apps/easybuild/software/EasyBuild/4.8.0/easybuild/easyconfigs, so using it...
CFGS1=/shared/apps/easybuild/software/EasyBuild/4.8.0/easybuild/easyconfigs
 * $CFGS1/b/bashplotlib/bashplotlib-0.6.5-GCCcore-10.3.0.eb
 * $CFGS1/h/HPL/HPL-2.1-foss-2016.04.eb
 * $CFGS1/h/HPL/HPL-2.1-foss-2016.06.eb
 * $CFGS1/h/HPL/HPL-2.1-foss-2016a.eb
 * $CFGS1/h/HPL/HPL-2.1-foss-2016b.eb
 ...
 * $CFGS1/h/HPL/HPL-2.3-foss-2022a.eb
 * $CFGS1/h/HPL/HPL-2.3-foss-2022b.eb
 * $CFGS1/h/HPL/HPL-2.3-foss-2023a.eb
 ...
 * $CFGS1/h/HPL/HPL-2.3-intel-2022b.eb
 * $CFGS1/h/HPL/HPL-2.3-intel-2023.03.eb
 * $CFGS1/h/HPL/HPL-2.3-intel-2023a.eb
 * $CFGS1/h/HPL/HPL-2.3-intelcuda-2019b.eb
 * $CFGS1/h/HPL/HPL-2.3-intelcuda-2020a.eb
 * $CFGS1/h/HPL/HPL-2.3-iomkl-2019.01.eb
 * $CFGS1/h/HPL/HPL-2.3-iomkl-2021a.eb
 * $CFGS1/h/HPL/HPL-2.3-iomkl-2021b.eb
 * $CFGS1/h/HPL/HPL_parallel-make.patch
```


From this list, you should select the version matching the target toolchain version -- here [foss-2022b](https://docs.easybuild.io/common-toolchains/#common_toolchains_update_cycle).

Once you pick a given recipy, install it with

       eb <name>.eb [-D] -r

* `-D` enables the dry-run mode to check what's going to be install -- **ALWAYS try it first**
* `-r` enables the robot mode to automatically install all dependencies while searching for easyconfigs in a set of pre-defined directories -- you can also prepend new directories to search for eb files (like the current directory `$PWD`) using the option and syntax `--robot-paths=$PWD:` (do not forget the ':'). See [Controlling the robot search path documentation](http://easybuild.readthedocs.io/en/latest/Using_the_EasyBuild_command_line.html#controlling-the-robot-search-path)
* The `$CFGS<n>/` prefix should be dropped unless you know what you're doing (and thus have previously defined the variable -- see the first output of the `eb -S [...]` command).

Let's try to review the missing dependencies from a dry-run :

``` bash
# Select the one matching the target software set version
(node)$ eb HPL-2.3-foss-2022b.eb -Dr   # Dry-run
== Temporary log file in case of crash /tmp/eb-lzv785be/easybuild-ihga94y0.log
== found valid index for /shared/apps/easybuild/software/EasyBuild/4.8.0/easybuild/easyconfigs, so using it...
== found valid index for /shared/apps/easybuild/software/EasyBuild/4.8.0/easybuild/easyconfigs, so using it...
Dry run: printing build status of easyconfigs and dependencies
CFGS=/shared/apps/easybuild/software/EasyBuild/4.8.0/easybuild/easyconfigs
 * [x] $CFGS/m/M4/M4-1.4.19.eb (module: devel/M4/1.4.19)
 * [x] $CFGS/b/Bison/Bison-3.8.2.eb (module: lang/Bison/3.8.2)
 * [x] $CFGS/f/flex/flex-2.6.4.eb (module: lang/flex/2.6.4)
 * [x] $CFGS/z/zlib/zlib-1.2.12.eb (module: lib/zlib/1.2.12)
 * [x] $CFGS/b/binutils/binutils-2.39.eb (module: tools/binutils/2.39)
 * [x] $CFGS/g/GCCcore/GCCcore-12.2.0.eb (module: compiler/GCCcore/12.2.0)
 * [x] $CFGS/z/zlib/zlib-1.2.12-GCCcore-12.2.0.eb (module: lib/zlib/1.2.12-GCCcore-12.2.0)
 * [x] $CFGS/h/help2man/help2man-1.49.2-GCCcore-12.2.0.eb (module: tools/help2man/1.49.2-GCCcore-12.2.0)
 * [x] $CFGS/m/M4/M4-1.4.19-GCCcore-12.2.0.eb (module: devel/M4/1.4.19-GCCcore-12.2.0)
 * [x] $CFGS/b/Bison/Bison-3.8.2-GCCcore-12.2.0.eb (module: lang/Bison/3.8.2-GCCcore-12.2.0)
 * [x] $CFGS/f/flex/flex-2.6.4-GCCcore-12.2.0.eb (module: lang/flex/2.6.4-GCCcore-12.2.0)
 * [x] $CFGS/b/binutils/binutils-2.39-GCCcore-12.2.0.eb (module: tools/binutils/2.39-GCCcore-12.2.0)
 * [x] $CFGS/p/pkgconf/pkgconf-1.9.3-GCCcore-12.2.0.eb (module: devel/pkgconf/1.9.3-GCCcore-12.2.0)
 * [x] $CFGS/g/groff/groff-1.22.4-GCCcore-12.2.0.eb (module: tools/groff/1.22.4-GCCcore-12.2.0)
 * [x] $CFGS/n/ncurses/ncurses-6.3-GCCcore-12.2.0.eb (module: devel/ncurses/6.3-GCCcore-12.2.0)
 * [x] $CFGS/e/expat/expat-2.4.9-GCCcore-12.2.0.eb (module: tools/expat/2.4.9-GCCcore-12.2.0)
 * [x] $CFGS/b/bzip2/bzip2-1.0.8-GCCcore-12.2.0.eb (module: tools/bzip2/1.0.8-GCCcore-12.2.0)
 * [x] $CFGS/g/GCC/GCC-12.2.0.eb (module: compiler/GCC/12.2.0)
 * [x] $CFGS/f/FFTW/FFTW-3.3.10-GCC-12.2.0.eb (module: numlib/FFTW/3.3.10-GCC-12.2.0)
 * [x] $CFGS/u/UnZip/UnZip-6.0-GCCcore-12.2.0.eb (module: tools/UnZip/6.0-GCCcore-12.2.0)
 * [x] $CFGS/l/libreadline/libreadline-8.2-GCCcore-12.2.0.eb (module: lib/libreadline/8.2-GCCcore-12.2.0)
 * [x] $CFGS/l/libtool/libtool-2.4.7-GCCcore-12.2.0.eb (module: lib/libtool/2.4.7-GCCcore-12.2.0)
 * [x] $CFGS/m/make/make-4.3-GCCcore-12.2.0.eb (module: devel/make/4.3-GCCcore-12.2.0)
 * [x] $CFGS/t/Tcl/Tcl-8.6.12-GCCcore-12.2.0.eb (module: lang/Tcl/8.6.12-GCCcore-12.2.0)
 * [x] $CFGS/p/pkgconf/pkgconf-1.8.0.eb (module: devel/pkgconf/1.8.0)
 * [x] $CFGS/s/SQLite/SQLite-3.39.4-GCCcore-12.2.0.eb (module: devel/SQLite/3.39.4-GCCcore-12.2.0)
 * [x] $CFGS/o/OpenSSL/OpenSSL-1.1.eb (module: system/OpenSSL/1.1)
 * [x] $CFGS/l/libevent/libevent-2.1.12-GCCcore-12.2.0.eb (module: lib/libevent/2.1.12-GCCcore-12.2.0)
 * [x] $CFGS/c/cURL/cURL-7.86.0-GCCcore-12.2.0.eb (module: tools/cURL/7.86.0-GCCcore-12.2.0)
 * [x] $CFGS/d/DB/DB-18.1.40-GCCcore-12.2.0.eb (module: tools/DB/18.1.40-GCCcore-12.2.0)
 * [x] $CFGS/p/Perl/Perl-5.36.0-GCCcore-12.2.0.eb (module: lang/Perl/5.36.0-GCCcore-12.2.0)
 * [x] $CFGS/a/Autoconf/Autoconf-2.71-GCCcore-12.2.0.eb (module: devel/Autoconf/2.71-GCCcore-12.2.0)
 * [x] $CFGS/a/Automake/Automake-1.16.5-GCCcore-12.2.0.eb (module: devel/Automake/1.16.5-GCCcore-12.2.0)
 * [x] $CFGS/a/Autotools/Autotools-20220317-GCCcore-12.2.0.eb (module: devel/Autotools/20220317-GCCcore-12.2.0)
 * [x] $CFGS/n/numactl/numactl-2.0.16-GCCcore-12.2.0.eb (module: tools/numactl/2.0.16-GCCcore-12.2.0)
 * [x] $CFGS/u/UCX/UCX-1.13.1-GCCcore-12.2.0.eb (module: lib/UCX/1.13.1-GCCcore-12.2.0)
 * [x] $CFGS/l/libfabric/libfabric-1.16.1-GCCcore-12.2.0.eb (module: lib/libfabric/1.16.1-GCCcore-12.2.0)
 * [x] $CFGS/l/libffi/libffi-3.4.4-GCCcore-12.2.0.eb (module: lib/libffi/3.4.4-GCCcore-12.2.0)
 * [x] $CFGS/x/xorg-macros/xorg-macros-1.19.3-GCCcore-12.2.0.eb (module: devel/xorg-macros/1.19.3-GCCcore-12.2.0)
 * [x] $CFGS/l/libpciaccess/libpciaccess-0.17-GCCcore-12.2.0.eb (module: system/libpciaccess/0.17-GCCcore-12.2.0)
 * [x] $CFGS/u/UCC/UCC-1.1.0-GCCcore-12.2.0.eb (module: lib/UCC/1.1.0-GCCcore-12.2.0)
 * [x] $CFGS/n/ncurses/ncurses-6.3.eb (module: devel/ncurses/6.3)
 * [x] $CFGS/g/gettext/gettext-0.21.1.eb (module: tools/gettext/0.21.1)
 * [x] $CFGS/x/XZ/XZ-5.2.7-GCCcore-12.2.0.eb (module: tools/XZ/5.2.7-GCCcore-12.2.0)
 * [x] $CFGS/p/Python/Python-3.10.8-GCCcore-12.2.0-bare.eb (module: lang/Python/3.10.8-GCCcore-12.2.0-bare)
 * [x] $CFGS/b/BLIS/BLIS-0.9.0-GCC-12.2.0.eb (module: numlib/BLIS/0.9.0-GCC-12.2.0)
 * [x] $CFGS/o/OpenBLAS/OpenBLAS-0.3.21-GCC-12.2.0.eb (module: numlib/OpenBLAS/0.3.21-GCC-12.2.0)
 * [x] $CFGS/l/libarchive/libarchive-3.6.1-GCCcore-12.2.0.eb (module: tools/libarchive/3.6.1-GCCcore-12.2.0)
 * [x] $CFGS/l/libxml2/libxml2-2.10.3-GCCcore-12.2.0.eb (module: lib/libxml2/2.10.3-GCCcore-12.2.0)
 * [x] $CFGS/c/CMake/CMake-3.24.3-GCCcore-12.2.0.eb (module: devel/CMake/3.24.3-GCCcore-12.2.0)
 * [ ] $CFGS/h/hwloc/hwloc-2.8.0-GCCcore-12.2.0.eb (module: system/hwloc/2.8.0-GCCcore-12.2.0)
 * [ ] $CFGS/p/PMIx/PMIx-4.2.2-GCCcore-12.2.0.eb (module: lib/PMIx/4.2.2-GCCcore-12.2.0)
 * [x] $CFGS/o/OpenMPI/OpenMPI-4.1.4-GCC-12.2.0.eb (module: mpi/OpenMPI/4.1.4-GCC-12.2.0)
 * [x] $CFGS/f/FlexiBLAS/FlexiBLAS-3.2.1-GCC-12.2.0.eb (module: lib/FlexiBLAS/3.2.1-GCC-12.2.0)
 * [x] $CFGS/g/gompi/gompi-2022b.eb (module: toolchain/gompi/2022b)
 * [x] $CFGS/f/FFTW.MPI/FFTW.MPI-3.3.10-gompi-2022b.eb (module: numlib/FFTW.MPI/3.3.10-gompi-2022b)
 * [x] $CFGS/s/ScaLAPACK/ScaLAPACK-2.2.0-gompi-2022b-fb.eb (module: numlib/ScaLAPACK/2.2.0-gompi-2022b-fb)
 * [x] $CFGS/f/foss/foss-2022b.eb (module: toolchain/foss/2022b)
 * [ ] $CFGS/h/HPL/HPL-2.3-foss-2022b.eb (module: tools/HPL/2.3-foss-2022b)
== Temporary log file(s) /tmp/eb-lzv785be/easybuild-ihga94y0.log* have been removed.
== Temporary directory /tmp/eb-lzv785be has been removed.
```
Let's try to install it (remove the `-D`):

``` bash
# Select the one matching the target software set version
(node)$ eb HPL-2.3-foss-2022b.eb -r
```
From now on, you should be able to see the new module.

```bash
(node)$  module spider HPL
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  tools/HPL: tools/HPL/2.3-foss-2022b
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Description:
      HPL is a software package that solves a (random) dense linear system in double precision (64 bits) arithmetic on distributed-memory computers. It can thus be regarded as a portable as well as freely available implementation of the High Performance Computing Linpack Benchmark.


    This module can be loaded directly: module load tools/HPL/2.3-foss-2022b

    Help:
      
      Description
      ===========
      HPL is a software package that solves a (random) dense linear system in double precision (64 bits)
       arithmetic on distributed-memory computers. It can thus be regarded as a portable as well as freely available
       implementation of the High Performance Computing Linpack Benchmark.
      
      
      More information
      ================
       - Homepage: https://www.netlib.org/benchmark/hpl/

```


**Tips**: When you load a module `<NAME>` generated by Easybuild, it is installed within the directory reported by the `$EBROOT<NAME>` variable.
In the above case, you will find the generated binary in `${EBROOTHPL}/`.






## Installing softwares with [Spack](ihttps://spack.io/)

* To do this, please clone the Spack GitHub repository into a `SPACK_ROOT` which is defined to be on a your project directory, i.e., `/shared/project/<project_id>`.

* Then add the configuration to you `~/.bashrc` file.

* You may wish to change the location of the` SPACK_ROOT` to fit your specific cluster configuration.

* Here, we consider the release v0.19 of Spack from the releases/v0.19 branch, however, you may wish to checkout the develop branch for the latest packages.

```bash
git clone -c feature.manyFiles=true -b releases/v0.19 https://github.com/spack/spack $SPACK_ROOT
```

* Then, add the following lines in your .bashrc

```bash
export PROJECT="/shared/projects/<project_id>"
export SPACK_ROOT="${PROJECT}/spack"
if [[ -f "${SPACK_ROOT}/share/spack/setup-env.sh" && -n ${SLURM_JOB_ID} ]];then
    source ${SPACK_ROOT}/share/spack/setup-env.sh" 
fi
```

!!! danger "Adapt accordingly"
    * Do **NOT** forget to replace `<project_id>` with your project name


## Spack Binary Cache

At [ISC'22](https://www.isc-hpc.com/), in conjunction with the Spack v0.18 release, AWS announced a collaborative effort to host a Binary Cache .
The binary cache stores prebuilt versions of common HPC packages, meaning that the installation process is reduced to relocation rather than compilation. To increase flexibility the binary cache contains package builds with different variants and built with different compilers.
The purpose of the binary cache is to drastically speed up package installation, especially when long dependency chains exist.


The binary cache is periodically updated with the latest versions of packages, and is released in conjunction with Spack releases. Thus you can use the v0.18 binary cache to have packages specifically from that Spack release. Alternatively, you can make use of the develop binary cache, which is kept up to date with the Spack develop branch.

* To add the develop binary cache, and trusting the associated gpg keys:

```bash
spack mirror add binary_mirror https://binaries.spack.io/develop
spack buildcache keys -it
```

## Installing packages

The notation for installing packages, when the binary cache has been enabled is unchanged. Spack will first check to see if the package is installable from the binary cache, and only upon failure will it install from source. We see confirmation of this in the output:

```bash
$ spack install bzip2
==> Installing bzip2-1.0.8-paghlsmxrq7p26qna6ml6au4fj2bdw6k
==> Fetching https://binaries.spack.io/develop/build_cache/linux-amzn2-x86_64_v4-gcc-7.3.1-bzip2-1.0.8-paghlsmxrq7p26qna6ml6au4fj2bdw6k.spec.json.sig
gpg: Signature made Fri 01 Jul 2022 04:21:22 AM UTC using RSA key ID 3DB0C723
gpg: Good signature from "Spack Project Official Binaries <maintainers@spack.io>"
==> Fetching https://binaries.spack.io/develop/build_cache/linux-amzn2-x86_64_v4/gcc-7.3.1/bzip2-1.0.8/linux-amzn2-x86_64_v4-gcc-7.3.1-bzip2-1.0.8-paghlsmxrq7p26qna6ml6au4fj2bdw6k.spack
==> Extracting bzip2-1.0.8-paghlsmxrq7p26qna6ml6au4fj2bdw6k from binary cache
[+] /shared/spack/opt/spack/linux-amzn2-x86_64_v4/gcc-7.3.1/bzip2-1.0.8-paghlsmxrq7p26qna6ml6au4fj2bdw6k
```

## Bypassing the binary cache

* Sometimes we might want to install a specific package from source, and bypass the binary cache. To achieve this we can pass the `--no-cache` flag to the install command. We can use this notation to install cowsay.
```bash
spack install --no-cache cowsay
```

* To compile any software we are going to need a compiler. Out of the box Spack does not know about any compilers on the system. To list your registered compilers, please use the following command:
```bash
spack compiler list
```

It will return an empty list the first time you used after installing Spack
```bash
 ==> No compilers available. Run `spack compiler find` to autodetect compilers
```

* AWS ParallelCluster installs GCC by default, so you can ask Spack to discover compilers on the system:
```bash
spack compiler find
```

This should identify your GCC install. In your case a conmpiler should be found.
```bash
==> Added 1 new compiler to /home/ec2-user/.spack/linux/compilers.yaml
     gcc@7.3.1
 ==> Compilers are defined in the following files:
     /home/ec2-user/.spack/linux/compilers.yaml
```

## Install other compilers

This default GCC compiler may be sufficient for many applications, we may want to install a newer version of GCC or other compilers in general. Spack is able to install compilers like any other package.


## Newer GCC version

For example we can install a version of GCC 11.2.0, complete with binutils, and then add it to the Spack compiler list.
```·bash
spack install -j [num cores] gcc@11.2.0+binutils
spack load gcc@11.2.0
spack compiler find
spack unload
```
As Spack is building GCC and all of the dependency packages this install can take a long time (>30 mins).

## Arm Compiler for Linux

The Arm Compiler for Linux (ACfL) can be installed by Spack on Arm systems, like the Graviton2 (C6g) or Graviton3 (C7g).o
```bash
spack install arm@22.0.1
spack load arm@22.0.1
spack compiler find
spack unload
```

## Where to build softwares

The cluster has quite a small headnode, this means that the compilation of complex software is prohibited. One simple solution is to use the compute nodes to perform the Spack installations, by submitting the command through Slurm.
```bash
srun -N1 -c 36 spack install -j36 gcc@11.2.0+binutils
```

## AWS Environment

* The versions of these external packages may change and are included for reference.

* The Cluster comes pre-installed with [Slurm](https://slurm.schedmd.com/) , [libfabric](https://ofiwg.github.io/libfabric/) , [PMIx](https://pmix.github.io/standard) , [Intel MPI](https://www.intel.com/content/www/us/en/developer/tools/oneapi/mpi-library.html#gs.hvr8xx) , and [Open MPI](https://www.open-mpi.org/) . To use these packages, you need to tell spack where to find them.
```bash
cat << EOF > $SPACK_ROOT/etc/spack/packages.yaml
packages:
    libfabric:
        variants: fabrics=efa,tcp,udp,sockets,verbs,shm,mrail,rxd,rxm
        externals:
        - spec: libfabric@1.13.2 fabrics=efa,tcp,udp,sockets,verbs,shm,mrail,rxd,rxm
          prefix: /opt/amazon/efa
        buildable: False
    openmpi:
        variants: fabrics=ofi +legacylaunchers schedulers=slurm ^libfabric
        externals:
        - spec: openmpi@4.1.1 %gcc@7.3.1
          prefix: /opt/amazon/openmpi
        buildable: False
    pmix:
        externals:
          - spec: pmix@3.2.3 ~pmi_backwards_compatibility
            prefix: /opt/pmix
        buildable: False
    slurm:
        variants: +pmix sysconfdir=/opt/slurm/etc
        externals:
        - spec: slurm@21.08.8-2 +pmix sysconfdir=/opt/slurm/etc
          prefix: /opt/slurm
        buildable: False
    armpl:
        externals:
        - spec: armpl@21.0.0%gcc@9.3.0
          prefix: /opt/arm/armpl/21.0.0/armpl_21.0_gcc-9.3/
        buildable: False
EOF
```

## Add the GCC 9.3 Compiler

The Graviton image ships with an additional compiler within the ArmPL project. We can add this compiler to the Spack environment with the following command: `spack compiler add /opt/arm/armpl/gcc/9.3.0/bin/`

## Open MPI

For Open MPI we have already made the definition to set libfabric as a dependency of Open MPI. So by default it will configure it correctly.
```bash
spack install openmpi%gcc@11.2.0
```


## Additional resources

* Job submission relies on the Slurm scheduler. Please refer to the following [page](../jobs/submit.md) for more details.
* [Spack tutorial on AWS ParallelCluster](https://catalog.us-east-1.prod.workshops.aws/workshops/dd0ffcb3-ffc1-4b58-8c4b-09f9846549c7/en-US)












