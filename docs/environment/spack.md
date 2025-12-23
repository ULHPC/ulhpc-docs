# Spack

<!--intro-start-->

<!--[Spack](https://spack.io/about/) is an open-source package manager designed for installing, building, and managing scientific software across a wide range of system including from personal computers to super computers. It supports multiple versions, compilers, and configurations of software packages, all coexisting in a single system without conflict. Spack provides with [over 8,500 ](https://packages.spack.io/)official software packages available since the `v1.0.0` release.Additionally users can also create [custom packages](https://spack-tutorial.readthedocs.io/en/latest/tutorial_packaging.html) via `package.py` files for software not yet available in the Spack pre-defined [packages](https://spack.readthedocs.io/en/latest/package_fundamentals.html).# PREVIOUS VERSION-->

[Spack](https://spack.io/about/) is an open-source package manager designed for installing, building, and managing software on High Performance Computing systems. It facilitates the efficient installation of software packages with an added emphasis on flexibility, as it allows for an extensive and easy customization of dependencies through command line options. It provides a large number of software packages ([more than 8,600](https://packages.spack.io/) since `v.1.0.0` release), and supports multiple versions, compilers, and configurations, all of which can coexist in a single system without conflict.

<!-- Similar to [EasyBuild](https://docs.easybuild.io/), [Spack](https://spack.io/about/) is also available on the UL HPC platform for managing and installing scientific software in more flexible and customizable way.
At present, the UL HPC environment includes a pre-installed version of Spack,namely `devel/Spack/0.21.2` which can be accessed via the module system. -->

??? question "Why use automatic building tools like [Easybuild](https://docs.easybuild.io) or [Spack](https://spack.io/) on HPC environments?"
    
	While it may seem obvious to some of you, scientific software is often surprisingly difficult to build. Not all software packages rely on standard building tools like Autotools/Automake (the famous `configure; make; make install`) or CMake. Even with standard building tools, parsing the available option to ensure that the build matches the underlying hardware is time consuming and error-prone. Furthermore, scientific software often contains hardcoded build parameters or the documentation on how to optimize the build is poorly maintained.

    Software build and installation frameworks like Easybuild or Spack allow reproducible builds, handle complex dependency trees, and automatically generate corresponding environment modulefiles (e.g., LMod) for easy usage. In the ULHPC platform, EasyBuild is the primary tool used to ensure optimized software builds. However, Spack is also available and can be valuable in more flexible or user-driven contexts.Spack Some HPC sites use both [1]. 

    _Resources_

    1. See this [talk](https://www.archer2.ac.uk/training/courses/200617-spack-easybuild/) by William Lucas at EPCC for instance.

??? question "[Spack](https://spack.io/) or [Easybuild](https://docs.easybuild.io)? Use cases"
    <!--https://easybuild.io/eum22/009_eum22_spack_vs_easybuild.pdf-->
	
	In theory, Spack and Easybuild are two different software management frameworks for HPC systems. As such, they may be seen as direct competitors. In practice, however, their distinct features make each one well-suited for different tasks within the ULHPC cluster. 
	
	Easybuild mainly focuses on stability and robustness. It provides a user-facing software stack built out of the same common toolchain and based on stable versions. For these reasons, it has been the main framework to manage the software set on ULHPC for several years. 
	
	On the other hand, Spack is designed to provide flexibilty and easy-to-tweak software installations. These features make Spack particularly suitable for personal or software development setups, where users can easily tweak software installations via command line by selecting specific compilers, enabling/disabling features like MPI or CUDA, or managing large and complex dependency chains. Additionally, Spack supports user-level installations, allowing users to create isolated environments without administrative privileges. In the context of the ULHPC cluster, Spack is particularly suitable for setting up user and experimental software environments, in cases where the required software is not included in the software stack or when it is necessary to build multiple configurations of the same software, as in software development. 


## Pivot elements of Spack

### Spec syntax
Thanks to its [spec syntax](https://spack.readthedocs.io/en/latest/spec_syntax.html), Spack offers extensive and easy-to-tweak customization of software installations. The constraints used to install a specific configuration of a software package are referred to as *specs*. These can be used to specify multiple options such as the compiler version, compile options, architecture, microarchitecture, direct and transitive dependencies, and even Git versions. Its recursive syntax allows these elements to be combined in many ways, enabling the installation of highly specific software configurations. The strength of this syntax is illustrated in the example below, which shows how to use these constraints to specify an installation of `mpileaks`:
``` { .sh .copy }
spack install mpileaks@1.2:1.4 +debug ~qt target=x86_64_v3 %gcc@15 ^libelf@1.1 %clang@20
```
Package versions are selected after `@`. Direct dependencies are selected after the `%` sigil and transitive dependencies after the `^` sigil. By just combining all of them, we can target a very specific installation of `mpileaks` software.

### YAML files	

All Spack configuration settings are done via [configuration files](https://spack.readthedocs.io/en/latest/configuration.html) written in  [YAML](https://yaml.org/) format. Configuration files in Spack are defined by their precedence order and allow for multiple configuration scopes, where the user environment and the user configuration folder are the scopes with the highest precedence by default.

## Spack in ULHPC

Spack is part of the ULHPC software set. In the latest release (`2023b`), an environment module for `0.21.2` version of Spack is provided.
The recommended approach for building software with Spack on the ULHPC cluster is to use this environment module. It is configured to provide a working Spack interface including the most relevant libraries used to build scientific software. Moreover, it also avoids the generationof multiple files in the `$HOME` directory of the user, since the the Spack package list is already preloaded in the Spack root directory. 

### Setting up Spack.

!!! warning "Connect to a compute node"

    For all tests and compilation with Spack, it is essential to run on a [**compute node**](../systems/iris/compute.md), not in the [**login/access**](../connect/access.md). For detailed information on resource allocation and job submission, visit the [**Slurm Job Management System**](../slurm/index.md).

Running an [**interactive job**](../systems/iris/compute.md) on the cluster, the first step to create a Spack environment is to load the environment module:

```{ .sh .copy }
 module load devel/Spack/0.21.2 
```

??? note "Verfifying Spack shell support"
	
	By default, the setup-env.sh script is sourced when the Spack module is loaded, setting up Spack's shell support. To checkup that the environment has been correctly setup, the following command is executed:
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
 
We can check the multiple [configuration scopes](https://spack.readthedocs.io/en/latest/configuration.html#configuration-files) available, displayed from highest to lowest precedence order:

```{ .sh .copy }
spack config scopes -p
Scope           Path
command_line     
spack           /mnt/aiongpfs/users/jdelgadoguerrero/.local/easybuild/software/Spack/1.1.0/etc/spack/
user            /home/users/jdelgadoguerrero/.spack/
site            /mnt/aiongpfs/users/jdelgadoguerrero/.local/easybuild/software/Spack/1.1.0/etc/spack/site/
defaults        /mnt/aiongpfs/users/jdelgadoguerrero/.local/easybuild/software/Spack/1.1.0/etc/spack/defaults/
defaults:linux  /mnt/aiongpfs/users/jdelgadoguerrero/.local/easybuild/software/Spack/1.1.0/etc/spack/defaults/linux/
defaults:base   /mnt/aiongpfs/users/jdelgadoguerrero/.local/easybuild/software/Spack/1.1.0/etc/spack/defaults/base/
_builtin
```

The highest scope corresponds to the `$EBROOTSPACK/etc/spack`. This setup is intended for *single-user* or *project-specific* installations of Spack. The second highest scope corresponds to the `~/.spack` folder which is automatically created in your `$HOME` sdirectory when the module is loaded. This implies that any [configuration file](https://spack.readthedocs.io/en/latest/configuration.html) placed in that folder has precedence over any other scope, offering the possibility of easily configure and customize Spack at the user level. 

The YAML file responsible of basic configuration options is the `config.yaml`. A minimum version of the `config.yaml` can be found on `$EBROOTSPACK/etc/spack/site/`. It can be copied to the `~/.spack` via the following command:

```{ .sh .copy }
cp $EBROOTSPACK/etc/spack/site/config.yaml  ~/.spack/.
```

#### Define System-Provided Packages

Package settings are determined in Spack through [`packages.yaml`](https://spack.readthedocs.io/en/latest/packages_yaml.html) configuration file. Following  [spec syntax](https://spack.readthedocs.io/en/latest/spec_syntax.html), Spack allows fine-grained control over how software is built. This enables users to choose preferred implementations for virtual dependencies, select specific compilers, and configure Spack to use external software already installed on the ULHPC cluster, thus avoiding the need to rebuild everything from source at the `$HOME` directory.

!!! question "Why is it crucial for users to define external packages in packages.yaml?"

    While Spack can build everything from source, fundamental libraries like [MPI](../software/swsets/mpi.md) and [BLAS](https://www.netlib.org/blas/)/[LAPACK](https://www.netlib.org/lapack/)are often highly optimized and meticulously tuned by system administrators to leverage the specific hardware capabilities of the HPC clusters (e.g., network interconnects, CPU features, GPU architectures).

    Using Spack's generic builds for these core libraries often results in sub-optimal performance compared to the finely-tuned system-provided versions. Declaring optimized external packages in `packages.yaml` ensures that Spack-built applications link against the most performant versions available in the [ULHPC software collection](https://hpc-docs.uni.lu/software/), thereby maximizing the efficiency of scientific computations. This avoids the overhead of rebuilding everything from source unnecessarily and guarantees users code benefits from HPC system's specialized hardware optimizations.

A `packages.yaml` file is provided via `$EBROOTSPACK/etc/spack/site/packages.yaml`. It contains the configuration of different external system build dependencies, as well as the `GCC`and `LLVM`compilers provided in the `2023b` release. Moreover, it also contains all the packages corresponding to the `2023b` *foss* common compiler toolchain and other relevant packages to compile scientific code. During a Spack software installation, the software packages specified in `packages.yaml` are labeled as externals and Spack automatically loads its corresponding environment module. To do so, the module name must be specified in the package configuration. For example, the GCC compiler was added to `packages.yaml` with the following specifications:

```yaml
 gcc:
    externals:
    - spec: gcc@13.3.0 languages:='c,c++,fortran'
      prefix: /opt/apps/easybuild/systems/aion/rhel810-20251006/2024a/epyc/software/GCCcore/13.3.0
      modules:
      - compiler/GCC/13.3.0
      extra_attributes:
        compilers:
          c: /opt/apps/easybuild/systems/aion/rhel810-20251006/2024a/epyc/software/GCCcore/13.3.0/bin/gcc
          cxx: /opt/apps/easybuild/systems/aion/rhel810-20251006/2024a/epyc/software/GCCcore/13.3.0/bin/g++
          fortran: /opt/apps/easybuild/systems/aion/rhel810-20251006/2024a/epyc/software/GCCcore/13.3.0/bin/gfortran
    buildable: false
``` 
With this setup, Spack labels the GCC compuler as external, and will load the corresponding module during the installation of software buitlt under GCC. Moreovee, it also has been labeled as not buildable, which implies that Spack will not try to build the package unless it is forced to do it. The list of the available compilers detected by Spack can be displayed through the command `spack compiler list`. 

In order to customize the packages settings at the user level scope, `$EBROOTSPACK/etc/spack/site/packages.yaml` can be copied onto the `~/.spack` folder. Alternatively, a new `packages.yaml` file can be created in `~/.spack` to add new external packages or override ``$EBROOTSPACK/etc/spack/site` configuration. 

The process of [adding external packages](https://spack.readthedocs.io/en/latest/packages_yaml.html#packages-config) to the user settings can be automated as follows:

```
module load $package_module

spack external find --not-buildable $package_name@version
```

(Next:compilers)
