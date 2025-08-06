# Spack: A Package Manager on the UL HPC Platform

<!--intro-start-->

## Introduction to Spack

[Spack](https://spack.io/about/) is an open-source package manager designed for installing, building, and managing scientific software across a wide range of system including from personal computers to super computers. It supports multiple versions, compilers, and configurations of software packages, all coexisting in a single system without conflict. Spack provides with [over 8,500 ](https://packages.spack.io/)official software packages available since the `v1.0.0` release.Additionally users can also create [custom packages](https://spack-tutorial.readthedocs.io/en/latest/tutorial_packaging.html) via `package.py` files for software not yet available in the Spack pre-defined [packages](https://spack.readthedocs.io/en/latest/package_fundamentals.html).


<!-- Similar to [EasyBuild](https://docs.easybuild.io/), [Spack](https://spack.io/about/) is also available on the UL HPC platform for managing and installing scientific software in more flexible and customizable way.
At present, the UL HPC environment includes a pre-installed version of Spack,namely `devel/Spack/0.21.2` which can be accessed via the module system. -->

??? question "Why use automatic building tools like [Easybuild](https://docs.easybuild.io) or [Spack](https://spack.io/) on HPC environments?"

    While it may seem obvious to some of you, scientific software is often surprisingly difficult to build. Not all software packages rely on standard building tools like Autotools/Automake (the famous `configure; make; make install`) or CMake. Even with standard building tools, parsing the available option to ensure that the build matches the underlying hardware is time consuming and error-prone. Furthermore, scientific software often contains hardcoded build parameters or the documentation on how to optimize the build is poorly maintained.

    Software build and installation frameworks like Easybuild or Spack allow reproducible builds, handle complex dependency trees, and automatically generate corresponding environment modulefiles (e.g., LMod) for easy usage. In the ULHPC platform, EasyBuild is the primary tool used to ensure optimized software builds. However, Spack is also available and can be valuable in more flexible or user-driven contexts.Spack Some HPC sites use both [1]. 

    _Resources_

    1. See this [talk](https://www.archer2.ac.uk/training/courses/200617-spack-easybuild/) by William Lucas at EPCC for instance.

??? question "when should consider [Spack](https://spack.io/)?"

     While EasyBuild is the primary and most integrated software management system on ULHPC, there are specific scenarios where users should consider using Spack.

    Spack is particularly suitable when users need greater flexibility and customization in building software. For example, if a user requires selecting specific compilers, enabling/disabling features like MPI or CUDA, or managing large and complex dependency chains easily, Spack offers a more configurable environment than EasyBuild.While EasyBuild is often favored by HPC system administrators for its robust and repeatable system-wide deployments, Spack is more focused on HPC developers and advanced users due to its easier-to-tweak nature.

    Additionally, Spack supports user-level installations, allowing users to create isolated environments without administrative privileges, making it highly suitable for personal or experimental setups. Spack's environment definition files (e.g., spack.yaml) further enhance its utility by allowing users to precisely replicate the same software stack elsewhere.

    In essence, Spack is the better choice when customization, portability, or broader package availability are required beyond what EasyBuild typically offers.



## Setting up Spack.

!!! warning "Connect to a compute node"

    For all tests and compilation with Spack, it is essential to run on a [**compute node**](../systems/iris/compute.md), not in the [**login/access**](../connect/access.md). For detailed information on resource allocation and job submission, visit the [**Slurm Job Management System**](../slurm/index.md).


### Clone & Setup Spack

Cloning and setting up Spack in  `$HOME` directory is recommended, as it provides significantly better performance for handling small files compared to `$SCRATCH`.

To clone the Spack Repository: 

``` { .sh .copy }
cd $HOME
git clone --depth=2 --branch=releases/v1.0.0 https://github.com/spack/spack.git
```

Cloning the Spack repository creates a directory named spack, and by default, it uses the develop branch. However for improved stability  switching to the latest official [release](https://github.com/spack/spack/releases) is recommended. The current release tags at that time `v1.0.0`. and to checkout the most recent release `v1.0.0` : 

``` { .sh .copy }
cd spack
git checkout v1.0.0
```

To make Spack available in the shell session, source its environment setup script:

``` { .sh .copy }
source $HOME/spack/share/spack/setup-env.sh
```

For convenience, this line can be added to the .`bashrc` file to make Spack automatically available in every new shell session.



??? note "Verfifying Spack installtion"

    Once Spack is sourced, the following command should display the path to the Spack executable and confirming that the environment is correctly set up:
    ``` { .sh .copy }
    which spack
    ```
    !!! note "Expected output resembles:"
        
    ``` { .sh  }
    spack () 
          { 
              : this is a shell function from: /home/users/<username>/spack/share/spack/setup-env.sh;
              : the real spack script is here: /home/users/<username>/spack/bin/spack;
              _spack_shell_wrapper "$@";
              return $?
          }
    ```
    This confirms that Spack’s environment is correctly loaded and ready for use.
 

### Spack Configuration Scopes

Spack’s behavior is controlled by [configuration files](https://spack.readthedocs.io/en/latest/configuration.html) in different scopes, which determine settings like installation paths, compilers, and package preferences and so on.Spack’s default configuration settings reside in `$SPACK_ROOT/etc/spack/defaults`. Spack provides six distinct configuration scopes to handle this customization, applied in order of decreasing priority.

| Scope        | Directory                                      |
|--------------|------------------------------------------------|
| Environment  | In environment base directory (`spack.yaml`)   |
| Custom       | Custom directory, specified with `--config-scope` |
| User         | `~/.spack/`                                    |
| Site         | `$SPACK_ROOT/etc/spack/`                       |
| System       | `/etc/spack/`                                  |
| Defaults     | `$SPACK_ROOT/etc/spack/defaults/`              |

The user configuration scope, stored in `~/.spack/` is ideal for defining personal preferences, compiler settings, and package defaults that apply across multiple projects and environments.The settings of this scope affect all instances of Spack. For more details see the [official tutorials](https://spack-tutorial.readthedocs.io/en/isc22/tutorial_configuration.html#configs-tutorial)

###  Define System-Provided Packages

Spack allows fine-grained control over how software is built through the [`packages.yaml`](https://spack.readthedocs.io/en/latest/packages_yaml.html) configuration file. This enables users to choose preferred implementations for virtual dependencies, choose particular compilers, and even configure Spack to use external installed software that are already available on the system while avoiding the need to rebuild everything from source.

Spack’s build defaults are in the  `etc/spack/defaults/packages.yaml` file.Most commonly, users define custom preferences in a user-level [configuration Scopes](https://spack.readthedocs.io/en/latest/configuration.html#configuration-scopes), which should be placed at`~/.spack/packages.yaml`.

!!! question "Why is it crucial for users to define external packages in packages.yaml?"

    While Spack can build everything from source, fundamental libraries like [MPI](../software/swsets/mpi.md) and [BLAS](https://www.netlib.org/blas/)/[LAPACK](https://www.netlib.org/lapack/)are often highly optimized and meticulously tuned by system administrators to leverage the specific hardware capabilities of the HPC clusters (e.g., network interconnects, CPU features, GPU architectures).

    Using Spack's generic builds for these core libraries often results in sub-optimal performance compared to the finely-tuned system-provided versions. Declaring optimized external packages in `packages.yaml` ensures that Spack-built applications link against the most performant versions available in the [ULHPC software collection](https://hpc-docs.uni.lu/software/), thereby maximizing the efficiency of scientific computations. This avoids the overhead of rebuilding everything from source unnecessarily and guarantees users code benefits from HPC system's specialized hardware optimizations.


To create a `packages.yaml` file at the user-level configuration scope  `~/.spack/`: 


``` { .sh .copy }
mkdir -p $HOME/.spack/
touch $HOME/.spack/packages.yaml
```


Then, add the following contents, which instructs Spack to use system-provided versions of `GCC`, `binutils`, and `OpenMPI` configured with native fabrics:
``` { .sh .copy }
 packages:
  gcc:
    externals:
    - spec: gcc@13.2.0+binutils languages:='c,c++,fortran'
      modules:
      - compiler/GCC/13.2.0
      extra_attributes:
        compilers:
          c: /opt/apps/easybuild/systems/aion/rhel810-20250405/2023b/epyc/software/GCCcore/13.2.0/bin/gcc
          cxx: /opt/apps/easybuild/systems/aion/rhel810-20250405/2023b/epyc/software/GCCcore/13.2.0/bin/g++
          fortran: /opt/apps/easybuild/systems/aion/rhel810-20250405/2023b/epyc/software/GCCcore/13.2.0/bin/gfortran
    buildable: false
  binutils:
    externals:
    - spec: binutils@2.40
      modules:
      - tools/binutils/2.40-GCCcore-13.2.0
    buildable: false
  libevent:
    externals:
    - spec: libevent@2.1.12
      modules:
      - lib/libevent/2.1.12-GCCcore-13.2.0
    buildable: false
  libfabric:
    externals:
    - spec: libfabric@1.19.0
      modules:
      - lib/libfabric/1.19.0-GCCcore-13.2.0
    buildable: false
  libpciaccess:
    externals:
    - spec: libpciaccess@0.17
      modules:
      - system/libpciaccess/0.17-GCCcore-13.2.0
    buildable: false
  libxml2:
    externals:
    - spec: libxml2@2.11.5
      modules:
      - lib/libxml2/2.11.5-GCCcore-13.2.0
    buildable: false
  hwloc:
    externals:
    - spec: hwloc@2.9.2+libxml2
      modules:
      - system/hwloc/2.9.2-GCCcore-13.2.0
    buildable: false
  mpi:
    buildable: false
  munge:
    externals:
    - spec: munge@0.5.13
      prefix: /usr
    buildable: false
  numactl:
    externals:
    - spec: numactl@2.0.16
      modules:
      - tools/numactl/2.0.16-GCCcore-13.2.0
    buildable: false
  openmpi:
    variants: fabrics=ofi,ucx schedulers=slurm
    externals:
    - spec: openmpi@4.1.6
      modules:
      - mpi/OpenMPI/4.1.6-GCC-13.2.0
    buildable: false
  pmix:
    externals:
    - spec: pmix@4.2.6
      modules:
      - lib/PMIx/4.2.6-GCCcore-13.2.0
    buildable: false
  slurm:
    externals:
    - spec: slurm@23.11.10 sysconfdir=/etc/slurm
      prefix: /usr
    buildable: false
  ucx:
    externals:
    - spec: ucx@1.15.0
      modules:
      - lib/UCX/1.15.0-GCCcore-13.2.0
    buildable: false
  zlib:
    externals:
    - spec: zlib@1.2.13
      modules:
      - lib/zlib/1.2.13-GCCcore-13.2.0
    buildable: false

```
!!! note " Defining CUDA as an External Package"
    // i need to adjust that .

    Similarly, users can configure Spack to use a system-provided CUDA toolkit by adding the following example to the `packages.yaml` file. This helps Spack avoid rebuilding CUDA from source and ensures compatibility with the system GPU drivers and libraries:
    ``` { .sh .copy }
    packages:
      cuda:
        externals:
        - spec: 
          modules:
          - 
        buildable: false
    ```


## Installing softwares with Spack
!!! Note 
    In this section i will include examples and detailed instructions on how to install software using Spack and link to the relevant official documentation. 

### Spack Environments

A Spack [environment](https://spack.readthedocs.io/en/latest/environments.html) lets users manage software and dependencies in an isolated and reproducible way.

!!! info 
    On shared clusters, it's highly recommended to use Spack environments to keep installations clean, avoid conflicts, and and simplify sharing or reproduction.


To create and activate a Spack [environmen](https://spack.readthedocs.io/en/latest/environments.html):

``` { .sh .copy }
spack env create test-env
spack env activate test-env
```

This command creates a Spack environment in the directory `$SPACK_ROOT/var/spack/environments/test-env`. It also generates a `spack.yaml` file—the main configuration file where users specify packages to install, compilers to use, and  other settings specific to that `test-env` environment.For more details  see the official [Spack Environment Tutorial](https://spack-tutorial.readthedocs.io/en/latest/tutorial_environments.html).

### Spack Packages Installation: 

Spack makes it easy to install software [packages](https://spack-tutorial.readthedocs.io/en/pearc22/tutorial_packaging.html#what-is-a-spack-package) from its extensive repository. To [install any package](https://spack.readthedocs.io/en/latest/package_fundamentals.html#installing-and-uninstalling) listed by spack list, use the following command: `spack install <package_name>`


!!! details "Spack Packages Spec"

    Spack uses a specific syntax to describe [package](https://spack.readthedocs.io/en/latest/packaging_guide_creation.html#structure-of-a-package) configurations during installation. Each configuration is called a [spec](https://spack.readthedocs.io/en/latest/spec_syntax.html) — a concise way to define package versions, compiler choices, variants, and dependencies.

    ``` { .sh .copy }
    spack install hdf5@1.10.7 +mpi ^mpich@3.3.2 ^zlib@1.2.11 %gcc@13.2.0
    ```

    This installs `HDF5` package  in version `1.10.7` with MPI support, explicitly specifying `mpich` version 3.3.2 and `zlib` version 1.2.11 as dependencies, all built with GCC 13.2.0.

    <!-- ![](https://spack.readthedocs.io/en/latest/_images/spec_anatomy.svg) -->



### Creating your own packages


### Spack Binary Cache
