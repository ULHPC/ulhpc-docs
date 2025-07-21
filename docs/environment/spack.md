# Spack: A Package Manager on the UL HPC Platform

[<img width='400px' src='https://cdn.rawgit.com/spack/spack/develop/share/spack/logo/spack-logo-text.svg'/>](https://spack.readthedocs.io/en/latest/#)



## Introduction to Spack

<p style="text-align: justify;"> Spack is an open-source package manager designed for installing, building, and managing scientific software across a wide range of systems—from personal laptops to the world’s largest supercomputers. It supports multiple versions, compilers, and configurations of packages, all coexisting without conflict. Spack is especially popular in high-performance computing (HPC) environments due to its non-destructive installations, flexible dependency resolution, and robust support for complex software stacks. </p>

### Why spack ? 

<p style="text-align: justify;">Spack simplifies the software installation process in scientific computing. It uses a concise <code>spec</code> syntax to let users define versions, compilers, build options, and dependencies in a readable format. Package recipes in Spack are written in pure Python, allowing contributors to manage many builds with a single file. With over 8,500 official packages available, Spack offers great flexibility—and it's not limited to pre-existing packages. Users can create custom ( e.g. <code>package.py</code> ) files for software not yet available in the Spack pre-defined packages. <a href="https://spack.readthedocs.io/en/latest/" target="_blank">[1]</a> </p>

### Key Features of Spack
<ul style="text-align: justify;"> 

<li><strong>Multiple Versions & Configurations:</strong> Easily install multiple versions of the same software with different compilers or build options.</li> 

<li><strong>Custom Dependencies:</strong> Flexibly control dependencies, even choosing between alternative implementations.</li> 

<li><strong>Non-destructive Installs:</strong> New installations do not interfere with existing packages.</li> 

<li><strong>Package Coexistence:</strong> Different builds of the same software can live side by side.</li>

 <li><strong>Easy Package Creation:</strong> Write simple ( e.g. <code>package.py</code> ) files in Python to add new software to Spack.</li> 
 
 <li><strong>Virtual Environments:</strong> Create isolated environments for experiments or projects.</li> 
 
 </ul>


### Key Resources

Below are essential resources including its official documentation, usage guides, packaging tutorials, and community links:

=== "Important Resources"

    -  <a href="https://spack.readthedocs.io/en/latest/" target="_blank">**Official Documentation**</a>  

    -  <a href="https://spack-tutorial.readthedocs.io/en/latest/" target="_blank">**Spack Tutorial**</a>  

    - <a href="https://packages.spack.io/" target="_blank"> **Package Index**  </a> 

    -  <a href="https://spack.readthedocs.io/en/latest/package_fundamentals.html" target="_blank">**Package Fundamentals**</a>   

    - <a href="https://spack.readthedocs.io/en/latest/environments.html" target="_blank">**Spack Environments**</a>  

    - <a href="https://cache.spack.io/" target="_blank"> **Spack Build Cache** </a>  


=== "Additional Resources"

    - <a href="https://spack.readthedocs.io/en/latest/configuration.html" target="_blank">**Spack Configuration file **</a>  

    -  <a href="https://spack.readthedocs.io/en/latest/packaging_guide.html" target="_blank">**Advance Packaging Guide**</a> 

    - <a href="https://spack.readthedocs.io/en/latest/build_settings.html" target="_blank">**Concretization Settings**</a>  


    - <a href="https://github.com/spack/spack/discussions" target="_blank">**Spack Community & Discussions**</a>  

???+ tabs "Spack Resources"

    === "Important Resources"

        -  <a href="https://spack.readthedocs.io/en/latest/" target="_blank">**Official Documentation**</a>  

        -  <a href="https://spack-tutorial.readthedocs.io/en/latest/" target="_blank">**Spack Tutorial**</a>  


        -  <a href="https://spack.readthedocs.io/en/latest/package_fundamentals.html" target="_blank">**Package Fundamentals**</a>  

        - <a href="https://packages.spack.io/" target="_blank"> **Package Index**  </a>  

        - <a href="https://spack.readthedocs.io/en/latest/environments.html" target="_blank">**Spack Environments**</a>  

        
        - <a href="https://cache.spack.io/" target="_blank"> **Spack Build Cache** </a>  


    === "Additional Resources"

        - <a href="https://spack.readthedocs.io/en/latest/configuration.html" target="_blank">**Spack Configuration file **</a>  

        -  <a href="https://spack.readthedocs.io/en/latest/packaging_guide.html" target="_blank">**Advance Packaging Guide**</a>  

        - <a href="https://spack.readthedocs.io/en/latest/build_settings.html" target="_blank">**Concretization Settings**</a>  

        - <a href="https://github.com/spack/spack/discussions" target="_blank">**Spack Community & Discussions**</a>  





## Setting up Spack.


!!! note
    The guide is also applicable to other HPC clusters where users need to manage components such as MPI libraries, compilers, and other software through the `module` system.


### Connection to a compute node
For all tests and compilation with Spack, it is essential to run on a **compute node**, not in the login/access node. Here's an example of how to allocate an [interactive session](../jobs/interactive.md) in **Aion cluster**.

```{.sh .copy}
si -N 1 -n 16 -c 1 -t 0-02:00:00 # on iris: -C broadwell or -C skylake
```

??? note "Allocation Details"

    `si` is a shell function that wraps the `salloc` command to simplify interactive Slurm job allocation.  
    It stands for:

    ```bash
    salloc -p interactive --qos debug -C batch ${options}
    ```
    - `${options}`: any additional arguments passed to `si` (e.g., `-N`, `-n`, `-c`, `-t`, etc.)

    ```bash
    si -N 1 -n 16 -c 1 -t 0-02:00:00
    ```

    This allocates:

    - 1 node (`-N 1`)
    - 16 MPI tasks (`-n 16`)
    - 1 CPU per task (`-c 1`)
    - for a wall time of 2 hours (`-t 0-02:00:00`) 

    !!! info "Iris Cluster"

        On the **Iris** cluster, 

        - Use `-C broadwell` or  `-C skylake` 

        **Examples:**
        ```bash
        si -N 1 -n 16 -c 1 -t 0-02:00:00 -C broadwell
        ```


### Clone & Setup Spack

Cloning and setting up Spack in  `$HOME` directory is recommended, as it provides significantly better performance for handling small files compared to `$SCRATCH`.
To clone the Spack Repository: 

``` { .sh .copy }
cd $HOME
git clone --depth=2 https://github.com/spack/spack.git
cd spack
```
To make Spack available in the shell session, source its environment setup script:

``` { .sh .copy }
source $HOME/spack/share/spack/setup-env.sh
```
For convenience, this line can be added to the .`bashrc` file to make Spack automatically available in every new shell session.

??? note "Test some basic functionality"

    Once Spack is sourced, the installation can be verified and basic functionality explored using the following commands:

    **Check Spack Version:**
    ```sh
    # Displays the currently installed version of Spack
    spack --version 
    ```
    **Search for Available Packages:**
    ```sh
    # Lists all available packages in Spack
    spack list
    ```

    **Search for a specific one:**
    ```sh
    # Shows all packages whose names contain "cmake"
    spack list cmake
    ```

    **Find Installed Packages:**
    ```sh
    # Lists all currently installed packages
    spack find
    ```
    !!! note 

        If Spack was just installed, this list will likely be empty. Installed packages will appear here after the first successful build.
        
    For more details : 
    
      - <a href="https://spack-tutorial.readthedocs.io/en/latest/tutorial_basics.html#" target="_blank">**Spack Basic Tutorial.**</a>  

### Useful Spack Commands.


The following tables summarizes the basic commands for managing software packages with Spack, from searching and installation to managing the software environment.

| Spack Command                | Description                                                  |
|------------------------------|--------------------------------------------------------------|
|`spack list`|	Lists all available packages. |
|`spack list <package>` |	Searches for packages matching the name or keyword.|
|` spack info <package>` | displays detailed information about that package|
| `spack install <package>`    | Installs a new package on the cluster.                       |
| `spack uninstall <package>`  | Removes an installed package from the cluster.               |
| `spack load <package>`       | Makes a package ready for use in the current session.        |
| `spack unload <package>`     | Removes a package from the current session's environment.    |
| `spack versions <package>`   | Shows all available versions of a package for installation on the cluster. |
| `spack help` |	Displays general help and available subcommands. |
| `spack help <subcommand>` |	Shows help for a specific subcommand. |
|`spack config get`|	Shows current Spack configuration settings |
|`spack compiler find	`| Detects and registers available compilers on the system |
|`spack dependencies <package>`|	Lists dependencies of a package |

??? info "Further Reference"
    For a comprehensive list of commands and advanced usage options, refer to the official Spack documentation:<a href="https://spack.readthedocs.io/en/latest/command_index.html" target="_blank"><strong>Spack Command Index</strong></a>


### Spack Environments

A Spack environment is a powerful feature that allows users to manage sets of software packages, dependencies, and configurations in an isolated and reproducible way. 

Below is a list of commonly used Spack environment commands:

| Spack Command                      | Description                                                  |
|-----------------------------------|--------------------------------------------------------------|
| `spack env status`                | Displays the currently active Spack environment.             |
| `spack env list`                  | Lists all existing Spack environments.                       |
| `spack env create <env_name>`     | Creates a new Spack environment with the specified name.     |
| `spack env activate <env_name>`   | Activates the specified Spack environment.                   |
| `spack env deactivate`            | Deactivates the currently active environment.                |
|`spack concretize`|	Prepares a full dependency spec for an environment or package before install |
| `spack install --add <package>`   | Installs a package into the currently active environment.    |


??? info "Further Reference"
    For more technical details, see the official Spack documentation:<a href="https://spack.readthedocs.io/en/latest/environments.html" target="_blank"><strong>Spack Environments</strong></a>



### Define System-Provided Packages

Spack allows users to control how software is built using the`packages.yaml` configuration file. This enables users to choose preferred implementations for virtual dependencies (like MPI or BLAS/LAPACK), choose particular compilers, and even configure Spack to use external installed software that are already available on the system while avoiding the need to rebuild everything from source.<a href="https://spack.readthedocs.io/en/latest/packages_yaml.html#package-settings-packages-yaml" target="_blank">[2]</a> </p>Create a `packages.yaml` file under: `$HOME/.spack/packages.yaml` 


``` { .sh .copy }
touch $HOME/.spack/packages.yaml
```


with the following contents:

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
This tells Spack to use the system available GCC, binutils and OpenMPI with the native fabrics.

## Building FEniCS

Create an environment and install FEniCS
``` { .sh .copy }
cd ~
spack env create -d fenicsx-main-20230126/ 
spack env activate fenicsx-main-20230126/
spack add py-fenics-dolfinx@main fenics-dolfinx+adios2 adios2+python petsc+mumps
# Change @main to e.g. @0.7.2 in the above if you want a fixed version.
spack concretize
spack install -j16
``` 
or the same directly in `spack.yaml` in `$SPACK_ENV`

``` { .sh .copy }
spack:
  # add package specs to the `specs` list
  specs:
  - py-fenics-dolfinx@main
  - fenics-dolfinx@main+adios2
  - petsc+mumps
  - adios2+python
  view: true
  concretizer:
    unify: true
```
The following are also commonly used in FEniCS scripts and may be useful

``` { .sh .copy }
spack add gmsh+opencascade py-numba py-scipy py-matplotlib
```
It is possible to build a specific version (git ref) of DOLFINx. Note that the hash must be the full hash. It is best to specify appropriate git refs on all components.

``` { .sh .copy }
# This is a Spack Environment file.
#
# It describes a set of packages to be installed, along with
# configuration settings.
spack:
  # add package specs to the `specs` list
  specs:
  - fenics-dolfinx@git.4f575964c70efd02dca92f2cf10c125071b17e4d=main+adios2
  - py-fenics-dolfinx@git.4f575964c70efd02dca92f2cf10c125071b17e4d=main

  - py-fenics-basix@git.2e2a7048ea5f4255c22af18af3b828036f1c8b50=main
  - fenics-basix@git.2e2a7048ea5f4255c22af18af3b828036f1c8b50=main

  - py-fenics-ufl@git.b15d8d3fdfea5ad6fe78531ec4ce6059cafeaa89=main

  - py-fenics-ffcx@git.7bc8be738997e7ce68ef0f406eab63c00d467092=main

  - fenics-ufcx@git.7bc8be738997e7ce68ef0f406eab63c00d467092=main

  - petsc+mumps
  - adios2+python
  view: true
  concretizer:
    unify: true
```

It is also possible to build only the C++ layer using


``` { .sh .copy }
spack add fenics-dolfinx@main+adios2 py-fenics-ffcx@main petsc+mumps
```
To rebuild FEniCSx from main branches inside an existing environment


``` { .sh .copy }
spack install --overwrite -j16 fenics-basix py-fenics-basix py-fenics-ffcx fenics-ufcx py-fenics-ufl fenics-dolfinx py-fenics-dolfinx
```


## Testing the build

Quickly test the build with
``` { .sh .copy }
srun python -c "from mpi4py import MPI; import dolfinx"
```

## Using the build

See the uni.lu documentation for full details - using the environment should be as 
simple as adding the following where `...` is the name/folder of your environment.

``` { .sh .copy }
#!/bin/bash -l
source $HOME/spack/share/spack/setup-env.sh
spack env activate ...
```

## Known issues

Workaround for broken Python module find for gmsh on uni.lu cluster

``` { .sh .copy }

export PYTHONPATH=$SPACK_ENV/.spack-env/view/lib64/:$PYTHONPATH

```
Workaround for broken Python module find for adios2 (seems broken in Spack)

``` { .sh .copy }

export PYTHONPATH=$(find $SPACK_ENV/.spack-env -type d -name 'site-packages' | grep venv):$PYTHONPATH

```