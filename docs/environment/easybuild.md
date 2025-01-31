# Easybuild

<!--intro-start-->

[![](https://easybuild.readthedocs.io/en/latest/_static/easybuild_logo_alpha.png){:style="width:200px; float: right;"}](https://easybuild.readthedocs.io/)

[EasyBuild](https://docs.easybuild.io/) is a software build and installation framework that allows you to manage scientific and other software on High Performance Computing systems in an efficient way. A large number of scientific software are supported (at least [3670 supported software packages](https://docs.easybuild.io/version-specific/supported-software/) since the 4.9.4 release).[^1]


For several years now, Easybuild is used to [manage the ULHPC User Software Set](modules.md#ulhpc-toolchains-and-software-set-versioning) and generate automatically the module files available to you on our computational resources in either `release` (default) or `testing` (pre-release/testing) environment. This enables users to easily extend the global [software set](modules.md#ulhpc-toolchains-and-software-set-versioning) with their own local software builds, either stored within their [global home directory](../data/layout.md#global-home-directory-home), or preferably in a shared [project directory](../data/layout.md). Easybuild generates automatically module files compliant with the [ULHPC module setup](../environment/modules.md).

[^1]: See also "[What is EasyBuild?](https://docs.easybuild.io/en/latest/Introduction.html)".

<!--intro-end-->

??? question "Why use automatic building tools like [Easybuild](https://docs.easybuild.io) or [Spack](https://spack.io/) on HPC environments?"

    While it may seem obvious to some of you, scientific software is often surprisingly difficult to build. Not all software packages rely on standard building tools like Autotools/Automake (the famous `configure; make; make install`) or CMake. Even with standard building tools, parsing the available option to ensure that the build matches the underlying hardware is time consuming and error-prone. Furthermore, scientific software often contains hardcoded build parameters or the documentation on how to optimize the build is poorly maintained.

    Software build and installation frameworks like Easybuild or Spack automate and document software building, while generating also the LMod modulefiles. We select Easybuild as our primary building tool to ensure optimized builds. Some HPC sites use both [1]. Often though, simply documenting the build instructions in an organized manner is sufficient [2].

    _Resources_

    1. See this [talk](https://www.archer2.ac.uk/training/courses/200617-spack-easybuild/) by William Lucas at EPCC for instance.
    2. HPC-UK provides a large collection of system specific [build instructions notes](https://github.com/hpc-uk/build-instructions) which you can copy and adjust.

## Easybuild Concepts and terminology

[:fontawesome-solid-sign-in-alt: Official Easybuild Tutorial](https://easybuilders.github.io/easybuild-tutorial/){: .md-button .md-button--link}

EasyBuild relies on two main concepts, [toolchains](https://docs.easybuild.io/en/latest/Concepts_and_Terminology.html#toolchains) and [EasyConfig files](https://docs.easybuild.io/en/latest/Concepts_and_Terminology.html#easyconfig-files). A toolchain corresponds to a compiler and a set of libraries which are commonly used to build a software. The two main toolchains frequently used on the UL HPC platform are `foss` (Free and Open Source Software) and `intel` toolchains.

1. `foss` is based on the GCC compiler and on open-source libraries (OpenMPI, OpenBLAS, etc.).
2. `intel` is based on the [oneAPI Intel compiler suit](https://www.intel.com/content/www/us/en/developer/articles/technical/oneapi-what-is-it.html) and on Intel libraries, such as Intel MPI and Intel Math Kernel Library (MKL).

An [EasyConfig file](http://easybuild.readthedocs.io/en/latest/Writing_easyconfig_files.html) is a simple text file that describes the build process of a software. For most software that uses standard procedures (like `configure`, `make` and `make install`), this file is very simple. Many [EasyConfig files](https://github.com/easybuilders/easybuild-easyconfigs/tree/master/easybuild/easyconfigs) are already provided with EasyBuild.


## ULHPC Easybuild Configuration

To build software with [Easybuild](https://docs.easybuild.io/) compliant with the configuration of the ULHPC facility, you need to be aware of the following setup:

- [Modules](modules.md) tool (`${EASYBUILD_MODULES_TOOL}`): [Lmod](http://lmod.readthedocs.io/)
- [Module Naming Scheme](modules.md#module-naming-schemes) (`${EASYBUILD_MODULE_NAMING_SCHEME}`): we use the hierarchical organization where the software are classified/categorized under a pre-defined class.

These variables are defined at the global profile level, under `/etc/profile.d/ulhpc_resif.sh` on the compute nodes with environment variables:

```bash
export EASYBUILD_MODULES_TOOL=Lmod
export EASYBUILD_MODULE_NAMING_SCHEME=CategorizedModuleNamingScheme
```

### Configuring the build process 

All builds and installations are performed at user level, so you don't need the admin (i.e. `root`) rights. The Easybuild [prefix path](https://docs.easybuild.io/configuration/#prefix) for instance determines the location where the compiled software is configured and installed. You can configure EasyBuild variables such as the prefix path either through

- environment variables, like `${EASYBUILD_PREFIX}`, or
- with flags like `--prefix`.

You can change the prefix path either by exporting the environment variable

```bash
export EASYBUILD_PREFIX=/path/to/desired/location/easybuild
```

or by passing the flag

```bash
eb --prefix=/path/to/desired/location/easybuild
```

when calling EasyBuild.

!!! info "Flags and environment variable in EasyBuild"

    Each setting in EasyBuild can be controlled by an environment variable `${EASYBUILD_<NAME>}` or the corresponding option flag, `--<name>`, of the EasyBuild (`eb`) script. The flags take precedence over the corresponding environment variable.

When installing software with EasyBuild, the program automatically detects the modules loaded in the system and only compiles the missing modules in the location pointed by `${EASYBUILD_PREFIX}`. Both system modules and modules previously build by the user are detected by EasyBuild. The installed software effectively extends the [ULHPC software set](modules.md#ulhpc-toolchains-and-software-set-versioning) with your own local builds.

### Selecting the installation location

The installation path of locally compiled EasyBuild modules is by default a subdirectory of the EasyBuild prefix path, `${EASYBUILD_PREFIX}`,

```
${EASYBUILD_PREFIX}/${EASYBUILD_SUBDIR_SOFTWARE}
```

where

```
${EASYBUILD_SUBDIR_SOFTWARE} = software
```

by default. The default value of prefix path is

```
${HOME}/.local/easybuild
```

which implies that software is installed in you home directory by default. As a rule of thump,

- install any software on shared [project directories](../data/project.md), so that is can be shared by all project members and save space, by setting
  ```bash
  export EASYBUILD_PREFIX=${PROJECTHOME}/<name>/easybuild
  ```
  for a project `<name>`;
- install any software that is used by yourself only on your [home directory](../data/layout.md#global-home-directory-home); set explicitly
  ```bash
  export EASYBUILD_PREFIX=${HOME}/.local/easybuild
  ```
  or use the `--prefix` flag in case the default location is modified in the future.

### Configuring the structure of the installation directory

In order to integrate the modules that you create in your local directories seamlessly in the modules of the [software set](modules.md#ulhpc-toolchains-and-software-set-versioning) you need to set some environment variables. The default location where modules are stored is

```
${EASYBUILD_PREFIX}/${EASYBUILD_SUBDIR_MODULES}/${EASYBUILD_SUFFIX_MODULES_PATH}
```

where by default

- `${EASYBUILD_SUBDIR_MODULES} = modules` and
- `${EASYBUILD_SUFFIX_MODULES_PATH} = all`.

To access the compiled modules, you need to add the module path to the `${MODULEPATH}` environment variable. Add the variable to the module using the `use` sub-command of the [`module`](modules.md) environment management program:

```bash
module use ${EASYBUILD_PREFIX}/${EASYBUILD_SUBDIR_MODULES}/${EASYBUILD_SUFFIX_MODULES_PATH}
```

!!! tips "Structuring the module directory"

    The value

    ```
    ${EASYBUILD_MODULE_NAMING_SCHEME} = CategorizedModuleNamingScheme
    ```

    ensures that the modules will appear in the correct category along side the [software set](modules.md#ulhpc-toolchains-and-software-set-versioning) modules when loading the module directory with `module use`.

### Building optimized binaries

The advantage of EasyBuild over manual configuration and compilation of software is that it builds optimized binaries targeting the hardware used. If you build a single executable for all the architectures available in the UL HPC clusters you are achieving sub-par performance in all but the architecture for which your build is optimized. To help you configure your compilation, UL HPC systems export the following variables in all compute nodes,

- `${ULHPC_CLUSTER}` with values
    - `aion`: in [Aion](/systems/aion/compute/) compute nodes,
    - `iris`: in [Iris](/systems/iris/compute/) compute nodes;
- `${RESIF_ARCH}` with values
    - `epyc`: in Aion compute nodes;
    - `broadwell`: in Iris [Broadwell](/systems/iris/compute/#broadwell-compute-nodes) and [Skylake](/systems/iris/compute/#skylake-compute-nodes) compute nodes in the [batch partition](/slurm/partitions/#iris);[^2]
    - `skylake`: in Iris [large memory](/systems/iris/compute/#large-memory-compute-nodes) nodes;
    - `gpu`: in Iris [GPU](/systems/iris/compute/#multi-gpu-compute-nodes) nodes.

[^2]: We don't optimize the binaries for the Skylake architecture in the batch partition of Iris; jobs in Iris may use a mix of Broadwell and Skylake architectures, so we try to use the same binary in all machines.

!!! tips "Compiling against the optimized software set"

    When compiling your software you have to ensure that

    1. you are using the software set modules that are optimized for your target hardware, and
    2. you are installing in a location where only modules for the target hardware are installed.

To load the correct modules for the compilation, simply login to a session on a compute node and load the desired environment setting module with the command,
```
module load env/<environment type>/<environment name>
```
where by default the `env/release/default` is loaded implicitly at login. Then, set your prefix path in your `bashrc` to:

```bash
export EASYBUILD_PREFIX=<path to desired root directory>/easybuild/${ULHPC_CLUSTER}/<environment type>/<environment name>/${RESIF_ARCH}
```

!!! tips "Automatically load local modules when logging in to compute nodes"

    You can _optionally_ add the following to your `bashrc` to automatically load your modules in compute nodes,

    ```bash
    if command -v module >/dev/null 2>&1; then
        module use "<path to desired root directory>/easybuild/${ULHPC_CLUSTER}/<environment type>/<environment name>/${RESIF_ARCH}/modules/all"
    fi
    ```

    assuming that you used the default values for `${EASYBUILD_SUBDIR_MODULES}` and `${EASYBUILD_SUFFIX_MODULES_PATH}`.


## Installation and update of local Easybuild

The ULHPC software provides an EasyBuild module that can be loaded with the command:

```
module load tools/EasyBuild
```

You can use EasyBuild to bootstrap the installation of an up-to-date version of EasyBuild in your local module set. More detailed instructions are available in the [official documentation](https://docs.easybuild.io/installation/#eb_as_module).
