# Building [custom] software with EasyBuild on the UL HPC platform

[EasyBuild](http://easybuild.readthedocs.io) can be used to ease, automate and script the build of software on the [UL HPC](https://hpc.uni.lu) platforms.

Indeed, as researchers involved in many cutting-edge and hot topics, you probably have access to many theoretical resources to understand the surrounding concepts. Yet it should _normally_ give you a wish to test the corresponding software.
Traditionally, this part is rather time-consuming and frustrating, especially when the developers did not rely on a "regular" building framework such as [CMake](https://cmake.org/) or the [autotools](https://www.gnu.org/software/automake/manual/html_node/Autotools-Introduction.html) (_i.e._ with build instructions as `configure --prefix <path> && make && make install`).

And when it comes to have a build adapted to an HPC system, you are somehow _forced_ to make a custom build performed on the target machine to ensure you will get the best possible performance.
[EasyBuild](https://github.com/easybuilders/easybuild) is one approach to facilitate this step.

[<img width='150px' src='https://docs.easybuild.io/img/easybuild_logo_2022_vertical_dark_bg_transparent.png#only-dark'/>](https://easybuild.io/)

EasyBuild is a tool that allows to perform automated and reproducible compilation and installation of software. A large number of scientific software are supported (**[1504 supported software packages](http://easybuild.readthedocs.io/en/latest/version-specific/Supported_software.html)** in the last release 3.6.1) -- see also [What is EasyBuild?](http://easybuild.readthedocs.io/en/latest/Introduction.html)

All builds and installations are performed at user level, so you don't need the admin (i.e. `root`) rights.
The software are installed in your home directory (by default in `$HOME/.local/easybuild/software/`) and a module file is generated (by default in `$HOME/.local/easybuild/modules/`) to use the software.

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
- [EasyBuild tutorial](https://easybuilders.github.io/easybuild-tutorial/)
- [EasyBuild documentation](http://easybuild.readthedocs.io/)
- [What is EasyBuild?](http://easybuild.readthedocs.io/en/latest/Introduction.html)
- [Toolchains](https://github.com/easybuilders/easybuild/wiki/Compiler-toolchains)
- [EasyConfig files](http://easybuild.readthedocs.io/en/latest/Writing_easyconfig_files.html)
- [List of supported software packages](http://easybuild.readthedocs.io/en/latest/version-specific/Supported_software.html)

### a. Installation

* [the official instructions](http://easybuild.readthedocs.io/en/latest/Installation.html).

What is important for the installation of EasyBuild are the following variables:

* `EASYBUILD_PREFIX`: where to install **local** modules and software, _i.e._ `$HOME/.local/easybuild`
* `EASYBUILD_MODULES_TOOL`: the type of [modules](http://modules.sourceforge.net/) tool you are using, _i.e._ `LMod` in this case
* `EASYBUILD_MODULE_NAMING_SCHEME`: the way the software and modules should be organized (flat view or hierarchical) -- we're advising on `CategorizedModuleNamingScheme`

Add the following entries to your `~/.bashrc` (use your favorite CLI editor like `nano` or `vim`):

```bash
# Easybuild
export EASYBUILD_PREFIX=$HOME/.local/easybuild
export EASYBUILD_MODULES_TOOL=Lmod
export EASYBUILD_MODULE_NAMING_SCHEME=CategorizedModuleNamingScheme
# Use the below variable to run:
#    module use $LOCAL_MODULES
#    module load tools/EasyBuild
export LOCAL_MODULES=${EASYBUILD_PREFIX}/modules/all

alias ma="module avail"
alias ml="module list"
function mu(){
   module use $LOCAL_MODULES
   module load tools/EasyBuild
}
```

Then source this file to expose the environment variables:

```bash
$> source ~/.bashrc
$> echo $EASYBUILD_PREFIX
/home/users/<login>/.local/easybuild
```

Now let's install EasyBuild following the [official procedure](https://docs.easybuild.io/installation/#eb_as_module). Install EasyBuild in a temporary directory and use this temporary installation to build an EasyBuild module in your `$EASYBUILD_PREFIX`:

```bash
# pick installation prefix, and install EasyBuild into it
export EB_TMPDIR=/tmp/$USER/eb_tmp
python3 -m pip install --ignore-installed --prefix $EB_TMPDIR easybuild

# update environment to use this temporary EasyBuild installation
export PATH=$EB_TMPDIR/bin:$PATH
export PYTHONPATH=$(/bin/ls -rtd -1 $EB_TMPDIR/lib*/python*/site-packages | tail -1):$PYTHONPATH
export EB_PYTHON=python3

# install Easybuild in your $EASYBUILD_PREFIX
eb --install-latest-eb-release --prefix $EASYBUILD_PREFIX
```

Now you can use your freshly built software. The main EasyBuild command is `eb`:

```bash
$> eb --version             # expected ;)
-bash: eb: command not found

# Load the newly installed Easybuild
$> echo $MODULEPATH
/opt/apps/resif/data/stable/default/modules/all/

$> module use $LOCAL_MODULES
$> echo $MODULEPATH
/home/users/<login>/.local/easybuild/modules/all:/opt/apps/resif/data/stable/default/modules/all

$> module spider Easybuild
$> module load tools/EasyBuild       # TAB is your friend...
$> eb --version
This is EasyBuild 3.6.1 (framework: 3.6.1, easyblocks: 3.6.1) on host iris-001.
```

Since you are going to use quite often the above command to use locally built modules and load easybuild, an alias `mu` is provided and can be used from now on. Use it **now**.

```
$> mu
$> module avail     # OR 'ma'
```
To get help on the EasyBuild options, use the `-h` or `-H` option flags:

    $> eb -h
    $> eb -H

### b. Local vs. global usage

As you probably guessed, we are going to use two places for the installed software:

* local builds `~/.local/easybuild`          (see `$LOCAL_MODULES`)
* global builds (provided to you by the UL HPC team) in `/opt/apps/resif/data/stable/default/modules/all` (see default `$MODULEPATH`).

Default usage (with the `eb` command) would install your software and modules in `~/.local/easybuild`.

Before that, let's explore the basic usage of [EasyBuild](http://easybuild.readthedocs.io/) and the `eb` command.

```bash
# Search for an Easybuild recipy with 'eb -S <pattern>'
$> eb -S Spark
CFGS1=/opt/apps/resif/data/easyconfigs/ulhpc/default/easybuild/easyconfigs/s/Spark
CFGS2=/home/users/<login>/.local/easybuild/software/tools/EasyBuild/3.6.1/lib/python2.7/site-packages/easybuild_easyconfigs-3.6.1-py2.7.egg/easybuild/easyconfigs/s/Spark
 * $CFGS1/Spark-2.1.1.eb
 * $CFGS1/Spark-2.3.0-intel-2018a-Hadoop-2.7-Java-1.8.0_162-Python-3.6.4.eb
 * $CFGS2/Spark-1.3.0.eb
 * $CFGS2/Spark-1.4.1.eb
 * $CFGS2/Spark-1.5.0.eb
 * $CFGS2/Spark-1.6.0.eb
 * $CFGS2/Spark-1.6.1.eb
 * $CFGS2/Spark-2.0.0.eb
 * $CFGS2/Spark-2.0.2.eb
 * $CFGS2/Spark-2.2.0-Hadoop-2.6-Java-1.8.0_144.eb
 * $CFGS2/Spark-2.2.0-Hadoop-2.6-Java-1.8.0_152.eb
 * $CFGS2/Spark-2.2.0-intel-2017b-Hadoop-2.6-Java-1.8.0_152-Python-3.6.3.eb
```

### c. Build software using provided EasyConfig file

In this part, we propose to build [High Performance Linpack (HPL)](http://www.netlib.org/benchmark/hpl/) using EasyBuild.
HPL is supported by EasyBuild, this means that an EasyConfig file allowing to build HPL is already provided with EasyBuild.

First of all, let's check if that software is not available by default:

```
$> module spider HPL

Lmod has detected the following error: Unable to find: "HPL"
```

Then, search for available EasyConfig files with HPL in their name. The EasyConfig files are named with the `.eb` extension.

```bash
# Search for an Easybuild recipy with 'eb -S <pattern>'
$> eb -S HPL-2.2
CFGS1=/home/users/svarrette/.local/easybuild/software/tools/EasyBuild/3.6.1/lib/python2.7/site-packages/easybuild_easyconfigs-3.6.1-py2.7.egg/easybuild/easyconfigs/h/HPL
 * $CFGS1/HPL-2.2-foss-2016.07.eb
 * $CFGS1/HPL-2.2-foss-2016.09.eb
 * $CFGS1/HPL-2.2-foss-2017a.eb
 * $CFGS1/HPL-2.2-foss-2017b.eb
 * $CFGS1/HPL-2.2-foss-2018a.eb
 * $CFGS1/HPL-2.2-fosscuda-2018a.eb
 * $CFGS1/HPL-2.2-giolf-2017b.eb
 * $CFGS1/HPL-2.2-giolf-2018a.eb
 * $CFGS1/HPL-2.2-giolfc-2017b.eb
 * $CFGS1/HPL-2.2-gmpolf-2017.10.eb
 * $CFGS1/HPL-2.2-goolfc-2016.08.eb
 * $CFGS1/HPL-2.2-goolfc-2016.10.eb
 * $CFGS1/HPL-2.2-intel-2017.00.eb
 * $CFGS1/HPL-2.2-intel-2017.01.eb
 * $CFGS1/HPL-2.2-intel-2017.02.eb
 * $CFGS1/HPL-2.2-intel-2017.09.eb
 * $CFGS1/HPL-2.2-intel-2017a.eb
 * $CFGS1/HPL-2.2-intel-2017b.eb
 * $CFGS1/HPL-2.2-intel-2018.00.eb
 * $CFGS1/HPL-2.2-intel-2018.01.eb
 * $CFGS1/HPL-2.2-intel-2018.02.eb
 * $CFGS1/HPL-2.2-intel-2018a.eb
 * $CFGS1/HPL-2.2-intelcuda-2016.10.eb
 * $CFGS1/HPL-2.2-iomkl-2016.09-GCC-4.9.3-2.25.eb
 * $CFGS1/HPL-2.2-iomkl-2016.09-GCC-5.4.0-2.26.eb
 * $CFGS1/HPL-2.2-iomkl-2017.01.eb
 * $CFGS1/HPL-2.2-intel-2017.02.eb
 * $CFGS1/HPL-2.2-intel-2017.09.eb
 * $CFGS1/HPL-2.2-intel-2017a.eb
 * $CFGS1/HPL-2.2-intel-2017b.eb
 * $CFGS1/HPL-2.2-intel-2018.00.eb
 * $CFGS1/HPL-2.2-intel-2018.01.eb
 * $CFGS1/HPL-2.2-intel-2018.02.eb
 * $CFGS1/HPL-2.2-intel-2018a.eb
 * $CFGS1/HPL-2.2-intelcuda-2016.10.eb
 * $CFGS1/HPL-2.2-iomkl-2016.09-GCC-4.9.3-2.25.eb
 * $CFGS1/HPL-2.2-iomkl-2016.09-GCC-5.4.0-2.26.eb
 * $CFGS1/HPL-2.2-iomkl-2017.01.eb
 * $CFGS1/HPL-2.2-iomkl-2017a.eb
 * $CFGS1/HPL-2.2-iomkl-2017b.eb
 * $CFGS1/HPL-2.2-iomkl-2018.02.eb
 * $CFGS1/HPL-2.2-iomkl-2018a.eb
 * $CFGS1/HPL-2.2-pomkl-2016.09.eb
```

We are going to build HPL 2.2 against the `intel` toolchain, typically the 2017a version which is available by default on the platform.

Pick the corresponding recipy (for instance `HPL-2.2-intel-2017a.eb`), install it with

       eb <name>.eb [-D] -r

* `-D` enables the dry-run mode to check what's going to be install -- **ALWAYS try it first**
* `-r` enables the robot mode to automatically install all dependencies while searching for easyconfigs in a set of pre-defined directories -- you can also prepend new directories to search for eb files (like the current directory `$PWD`) using the option and syntax `--robot-paths=$PWD:` (do not forget the ':'). See [Controlling the robot search path documentation](http://easybuild.readthedocs.io/en/latest/Using_the_EasyBuild_command_line.html#controlling-the-robot-search-path)
* The `$CFGS<n>/` prefix should be dropped unless you know what you're doing (and thus have previously defined the variable -- see the first output of the `eb -S [...]` command).

So let's install `HPL` version 2.2 and **FIRST** check which dependencies are satisfied with `-Dr`:

```bash
$> eb HPL-2.2-intel-2017a.eb -Dr
== temporary log file in case of crash /tmp/eb-CTC2hq/easybuild-gfLf1W.log
Dry run: printing build status of easyconfigs and dependencies
CFGS=/home/users/svarrette/.local/easybuild/software/tools/EasyBuild/3.6.1/lib/python2.7/site-packages/easybuild_easyconfigs-3.6.1-py2.7.egg/easybuild/easyconfigs
 * [x] $CFGS/m/M4/M4-1.4.17.eb (module: devel/M4/1.4.17)
 * [x] $CFGS/b/Bison/Bison-3.0.4.eb (module: lang/Bison/3.0.4)
 * [x] $CFGS/f/flex/flex-2.6.0.eb (module: lang/flex/2.6.0)
 * [x] $CFGS/z/zlib/zlib-1.2.8.eb (module: lib/zlib/1.2.8)
 * [x] $CFGS/b/binutils/binutils-2.27.eb (module: tools/binutils/2.27)
 * [x] $CFGS/g/GCCcore/GCCcore-6.3.0.eb (module: compiler/GCCcore/6.3.0)
 * [x] $CFGS/m/M4/M4-1.4.18-GCCcore-6.3.0.eb (module: devel/M4/1.4.18-GCCcore-6.3.0)
 * [x] $CFGS/z/zlib/zlib-1.2.11-GCCcore-6.3.0.eb (module: lib/zlib/1.2.11-GCCcore-6.3.0)
 * [x] $CFGS/h/help2man/help2man-1.47.4-GCCcore-6.3.0.eb (module: tools/help2man/1.47.4-GCCcore-6.3.0)
 * [x] $CFGS/b/Bison/Bison-3.0.4-GCCcore-6.3.0.eb (module: lang/Bison/3.0.4-GCCcore-6.3.0)
 * [x] $CFGS/f/flex/flex-2.6.3-GCCcore-6.3.0.eb (module: lang/flex/2.6.3-GCCcore-6.3.0)
 * [x] $CFGS/b/binutils/binutils-2.27-GCCcore-6.3.0.eb (module: tools/binutils/2.27-GCCcore-6.3.0)
 * [x] $CFGS/i/icc/icc-2017.1.132-GCC-6.3.0-2.27.eb (module: compiler/icc/2017.1.132-GCC-6.3.0-2.27)
 * [x] $CFGS/i/ifort/ifort-2017.1.132-GCC-6.3.0-2.27.eb (module: compiler/ifort/2017.1.132-GCC-6.3.0-2.27)
 * [x] $CFGS/i/iccifort/iccifort-2017.1.132-GCC-6.3.0-2.27.eb (module: toolchain/iccifort/2017.1.132-GCC-6.3.0-2.27)
 * [x] $CFGS/i/impi/impi-2017.1.132-iccifort-2017.1.132-GCC-6.3.0-2.27.eb (module: mpi/impi/2017.1.132-iccifort-2017.1.132-GCC-6.3.0-2.27)
 * [x] $CFGS/i/iimpi/iimpi-2017a.eb (module: toolchain/iimpi/2017a)
 * [x] $CFGS/i/imkl/imkl-2017.1.132-iimpi-2017a.eb (module: numlib/imkl/2017.1.132-iimpi-2017a)
 * [x] $CFGS/i/intel/intel-2017a.eb (module: toolchain/intel/2017a)
 * [ ] $CFGS/h/HPL/HPL-2.2-intel-2017a.eb (module: tools/HPL/2.2-intel-2017a)
== Temporary log file(s) /tmp/eb-CTC2hq/easybuild-gfLf1W.log* have been removed.
== Temporary directory /tmp/eb-CTC2hq has been removed.
```

As can be seen, there is a single element to install and this has not been done so far (box not checked). All the dependencies are already present (box checked).
Let's really install the selected software -- you may want to prefix the `eb` command with the `time` to collect the installation time:

```bash
$> time eb HPL-2.2-intel-2017a.eb -r       # Remove the '-D' (dry-run) flags
== temporary log file in case of crash /tmp/eb-nub_oL/easybuild-J8sNzx.log
== resolving dependencies ...
== processing EasyBuild easyconfig /home/users/svarrette/.local/easybuild/software/tools/EasyBuild/3.6.1/lib/python2.7/site-packages/easybuild_easyconfigs-3.6.1-py2.7.egg/easybuild/easyconfigs/h/HPL/HPL-2.2-intel-2017a.eb
== building and installing tools/HPL/2.2-intel-2017a...
== fetching files...
== creating build dir, resetting environment...
== unpacking...
== patching...
== preparing...
== configuring...
== building...
== testing...
== installing...
== taking care of extensions...
== postprocessing...
== sanity checking...
== cleaning up...
== creating module...
== permissions...
== packaging...
== COMPLETED: Installation ended successfully
== Results of the build can be found in the log file(s) /home/users/svarrette/.local/easybuild/software/tools/HPL/2.2-intel-2017a/easybuild/easybuild-HPL-2.2-20180608.094831.log
== Build succeeded for 1 out of 1
== Temporary log file(s) /tmp/eb-nub_oL/easybuild-J8sNzx.log* have been removed.
== Temporary directory /tmp/eb-nub_oL has been removed.

real    0m56.472s
user    0m15.268s
sys     0m19.998s
```

Check the installed software:

```
$> module av HPL

------------------------- /home/users/<login>/.local/easybuild/modules/all -------------------------
   tools/HPL/2.2-intel-2017a

Use "module spider" to find all possible modules.
Use "module keyword key1 key2 ..." to search for all possible modules matching any of the "keys".

$> module spider HPL

----------------------------------------------------------------------------------------------------
  tools/HPL: tools/HPL/2.2-intel-2017a
----------------------------------------------------------------------------------------------------
    Description:
      HPL is a software package that solves a (random) dense linear system in double precision
      (64 bits) arithmetic on distributed-memory computers. It can thus be regarded as a portable
      as well as freely available implementation of the High Performance Computing Linpack Benchmark.

    This module can be loaded directly: module load tools/HPL/2.2-intel-2017a

    Help:

      Description
      ===========
      HPL is a software package that solves a (random) dense linear system in double precision
      (64 bits) arithmetic on distributed-memory computers. It can thus be regarded as a portable
      as well as freely available implementation of the High Performance Computing Linpack Benchmark.


      More information
      ================
       - Homepage: http://www.netlib.org/benchmark/hpl/

$> module show tools/HPL
---------------------------------------------------------------------------------------------------
   /home/users/svarrette/.local/easybuild/modules/all/tools/HPL/2.2-intel-2017a.lua:
---------------------------------------------------------------------------------------------------
help([[
Description
===========
HPL is a software package that solves a (random) dense linear system in double precision
(64 bits) arithmetic on distributed-memory computers. It can thus be regarded as a portable
as well as freely available implementation of the High Performance Computing Linpack Benchmark.


More information
================
 - Homepage: http://www.netlib.org/benchmark/hpl/
]])
whatis("Description: HPL is a software package that solves a (random) dense linear system in
 double precision (64 bits) arithmetic on distributed-memory computers. It can thus be regarded
 as a portable as well as freely available implementation of the High Performance Computing
 Linpack Benchmark.")
whatis("Homepage: http://www.netlib.org/benchmark/hpl/")
conflict("tools/HPL")
load("toolchain/intel/2017a")
prepend_path("PATH","/home/users/svarrette/.local/easybuild/software/tools/HPL/2.2-intel-2017a/bin")
setenv("EBROOTHPL","/home/users/svarrette/.local/easybuild/software/tools/HPL/2.2-intel-2017a")
setenv("EBVERSIONHPL","2.2")
setenv("EBDEVELHPL","/home/users/svarrette/.local/easybuild/software/tools/HPL/2.2-intel-2017a/easybuild/tools-HPL-2.2-intel-2017a-easybuild-devel")
```

**Note**: to see the (locally) installed software, the `MODULEPATH` variable should include the `$HOME/.local/easybuild/modules/all/` (of `$LOCAL_MODULES`) path (which is what happens when using `module use <path>` -- see the `mu` command)

You can now load the freshly installed module like any other:

```bash
$> module load tools/HPL
$> module list

Currently Loaded Modules:
  1) tools/EasyBuild/3.6.1                          7) mpi/impi/2017.1.132-iccifort-2017.1.132-GCC-6.3.0-2.27
  2) compiler/GCCcore/6.3.0                         8) toolchain/iimpi/2017a
  3) tools/binutils/2.27-GCCcore-6.3.0              9) numlib/imkl/2017.1.132-iimpi-2017a
  4) compiler/icc/2017.1.132-GCC-6.3.0-2.27        10) toolchain/intel/2017a
  5) compiler/ifort/2017.1.132-GCC-6.3.0-2.27      11) tools/HPL/2.2-intel-2017a
  6) toolchain/iccifort/2017.1.132-GCC-6.3.0-2.27
```

**Tips**: When you load a module `<NAME>` generated by Easybuild, it is installed within the directory reported by the `$EBROOT<NAME>` variable.
In the above case, you will find the generated binary for HPL in `${EBROOTHPL}/bin/xhpl`.

You may want to test the newly built HPL benchmark (you need to reserve at least 4 cores for that to succeed):

```bash
# In another terminal, connect to the cluster frontend
# Have an interactive job
############### iris cluster (slurm) ###############
(access-iris)$> si -n 4        # this time reserve for 4 (mpi) tasks
$> mu
$> module load tools/HPL
$> cd $EBROOTHPL
$> ls
$> cd bin
$> ls
$> srun -n $SLURM_NTASKS ./xhpl

```

Running HPL benchmarks requires more attention -- a [full tutorial](https://ulhpc-tutorials.readthedocs.io/en/latest/parallel/mpi/HPL/) is dedicated to it.
Yet you can see that we obtained HPL 2.2 without writing any EasyConfig file.


### d. Build software using a customized EasyConfig file

There are multiple ways to amend an EasyConfig file. Check the `--try-*` option flags for all the possibilities.

Generally you want to do that when the up-to-date version of the software you want is **not** available as a recipy within Easybuild.
For instance, a very popular building environment [CMake](https://blog.kitware.com/cmake-3-11-3-available-for-download/) has recently released a new version (3.11.3), which you want to give a try.

It is not available as module, so let's build it.

First let's check for available easyconfigs recipy if one exist for the expected version:

```
$> eb -S Cmake-3
[...]
 * $CFGS2/CMake-3.9.1.eb
 * $CFGS2/CMake-3.9.4-GCCcore-6.4.0.eb
 * $CFGS2/CMake-3.9.5-GCCcore-6.4.0.eb
```

We are going to reuse one of the latest EasyConfig available, for instance lets copy `$CFGS2/CMake-3.9.1.eb`

```bash
# Work in a dedicated directory
$> mkdir -p ~/software/CMake
$> cd ~/software/CMake

$> eb -S Cmake-3|less   # collect the definition of the CFGS2 variable
$> CFGS2=/home/users/svarrette/.local/easybuild/software/tools/EasyBuild/3.6.1/lib/python2.7/site-packages/easybuild_easyconfigs-3.6.1-py2.7.egg/easybuild/easyconfigs/c/CMake
$> cp $CFGS2/CMake-3.9.1.eb .
$> mv CMake-3.9.1.eb CMake-3.11.3.eb        # Adapt version suffix to the lastest realse
```

You need to perform the following changes (here: version upgrade, and adapted checksum)

```diff
--- CMake-3.9.1.eb      2018-06-08 10:56:24.447699000 +0200
+++ CMake-3.11.3.eb     2018-06-08 11:07:39.716672000 +0200
@@ -1,7 +1,7 @@
 easyblock = 'ConfigureMake'

 name = 'CMake'
-version = '3.9.1'
+version = '3.11.3'

 homepage = 'http://www.cmake.org'
 description = """CMake, the cross-platform, open-source build system.
@@ -11,7 +11,7 @@

 source_urls = ['http://www.cmake.org/files/v%(version_major_minor)s']
 sources = [SOURCELOWER_TAR_GZ]
-checksums = ['d768ee83d217f91bb597b3ca2ac663da7a8603c97e1f1a5184bc01e0ad2b12bb']
+checksums = ['287135b6beb7ffc1ccd02707271080bbf14c21d80c067ae2c0040e5f3508c39a']

 configopts = '-- -DCMAKE_USE_OPENSSL=1'
```

If the checksum is not provided on the [official software page](https://cmake.org/download/), you will need to compute it yourself by downloading the sources and collect the checksum:

```bash
$> gsha256sum ~/Download/cmake-3.11.3.tar.gz
287135b6beb7ffc1ccd02707271080bbf14c21d80c067ae2c0040e5f3508c39a  cmake-3.11.3.tar.gz
```

Let's build it:

```bash
$>  eb ./CMake-3.11.3.eb -Dr
== temporary log file in case of crash /tmp/eb-UX7APP/easybuild-gxnyIv.log
Dry run: printing build status of easyconfigs and dependencies
CFGS=/mnt/irisgpfs/users/<login>/software/CMake
 * [ ] $CFGS/CMake-3.11.3.eb (module: devel/CMake/3.11.3)
== Temporary log file(s) /tmp/eb-UX7APP/easybuild-gxnyIv.log* have been removed.
== Temporary directory /tmp/eb-UX7APP has been removed.
```

Dependencies are fine, so let's build it:

```bash
$> time eb ./CMake-3.11.3.eb -r
== temporary log file in case of crash /tmp/eb-JjF92B/easybuild-RjzRjb.log
== resolving dependencies ...
== processing EasyBuild easyconfig /mnt/irisgpfs/users/<login>/software/CMake/CMake-3.11.3.eb
== building and installing devel/CMake/3.11.3...
== fetching files...
== creating build dir, resetting environment...
== unpacking...
== patching...
== preparing...
== configuring...
== building...
== testing...
== installing...
== taking care of extensions...
== postprocessing...
== sanity checking...
== cleaning up...
== creating module...
== permissions...
== packaging...
== COMPLETED: Installation ended successfully
== Results of the build can be found in the log file(s) /home/users/<login>/.local/easybuild/software/devel/CMake/3.11.3/easybuild/easybuild-CMake-3.11.3-20180608.111611.log
== Build succeeded for 1 out of 1
== Temporary log file(s) /tmp/eb-JjF92B/easybuild-RjzRjb.log* have been removed.
== Temporary directory /tmp/eb-JjF92B has been removed.

real	7m40.358s
user	5m56.442s
sys	1m15.185s
```

**Note** you can follow the progress of the installation in a separate shell on the node:

Check the result:

```bash
$> module av CMake
```

That's all ;-)

**Final remaks**

This workflow (copying an existing recipy, adapting the filename, the version and the source checksum) covers most of the test cases.
Yet sometimes you need to work on a more complex dependency check, in which case you'll need to adapt _many_ eb files.
In this case, for each build, you need to instruct Easybuild to search for easyconfigs also in the current directory, in which case you will use:

```bash
$> eb <filename>.eb --robot=$PWD:$EASYBUILD_ROBOT -D
$> eb <filename>.eb --robot=$PWD:$EASYBUILD_ROBOT
```

--------------------------------------------------------
### (OLD) Build software using your own EasyConfig file

Below are obsolete instructions to write a full Easyconfig file, left for archiving and informal purposes.

For this example, we create an EasyConfig file to build GZip 1.4 with the GOOLF toolchain.
Open your favorite editor and create a file named `gzip-1.4-goolf-1.4.10.eb` with the following content:

    easyblock = 'ConfigureMake'
    
    name = 'gzip'
    version = '1.4'
    
    homepage = 'http://www.gnu.org/software/gzip/'
    description = "gzip (GNU zip) is a popular data compression program as a replacement for compress"
    
    # use the GOOLF toolchain
    toolchain = {'name': 'goolf', 'version': '1.4.10'}
    
    # specify that GCC compiler should be used to build gzip
    preconfigopts = "CC='gcc'"
    
    # source tarball filename
    sources = ['%s-%s.tar.gz'%(name,version)]
    
    # download location for source files
    source_urls = ['http://ftpmirror.gnu.org/gzip']
    
    # make sure the gzip and gunzip binaries are available after installation
    sanity_check_paths = {
                          'files': ["bin/gunzip", "bin/gzip"],
                          'dirs': []
                         }
    
    # run 'gzip -h' and 'gzip --version' after installation
    sanity_check_commands = [True, ('gzip', '--version')]


This is a simple EasyConfig. Most of the fields are self-descriptive. No build method is explicitely defined, so it uses by default the standard *configure/make/make install* approach.


Let's build GZip with this EasyConfig file:

    $> time eb gzip-1.4-goolf-1.4.10.eb
    
    == temporary log file in case of crash /tmp/eb-hiyyN1/easybuild-ynLsHC.log
    == processing EasyBuild easyconfig /mnt/nfs/users/homedirs/mschmitt/gzip-1.4-goolf-1.4.10.eb
    == building and installing base/gzip/1.4-goolf-1.4.10...
    == fetching files...
    == creating build dir, resetting environment...
    == unpacking...
    == patching...
    == preparing...
    == configuring...
    == building...
    == testing...
    == installing...
    == taking care of extensions...
    == packaging...
    == postprocessing...
    == sanity checking...
    == cleaning up...
    == creating module...
    == COMPLETED: Installation ended successfully
    == Results of the build can be found in the log file /home/users/mschmitt/.local/easybuild/software/base/gzip/1.4-goolf-1.4.10/easybuild/easybuild-gzip-1.4-20150624.114745.log
    == Build succeeded for 1 out of 1
    == temporary log file(s) /tmp/eb-hiyyN1/easybuild-ynLsHC.log* have been removed.
    == temporary directory /tmp/eb-hiyyN1 has been removed.
    
    real    1m39.982s
    user    0m52.743s
    sys     0m11.297s


We can now check that our version of GZip is available via the modules:

    $> module avail gzip
    
    --------- /mnt/nfs/users/homedirs/mschmitt/.local/easybuild/modules/all ---------
        base/gzip/1.4-goolf-1.4.10



## To go further into details

Please refer to the following pointers to get additionnal features:

- [EasyBuild homepage](http://easybuilders.github.io/easybuild)
- [EasyBuild tutorial](https://easybuilders.github.io/easybuild-tutorial/)
- [EasyBuild documentation](http://easybuilders.github.io/easybuild/)
- [Getting started](https://github.com/easybuilders/easybuild/wiki/Getting-started)
- [Using EasyBuild](https://github.com/easybuilders/easybuild/wiki/Using-EasyBuild)
- [Step-by-step guide](https://github.com/easybuilders/easybuild/wiki/Step-by-step-guide)
